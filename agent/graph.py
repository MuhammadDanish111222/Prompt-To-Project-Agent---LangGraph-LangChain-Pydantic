from dotenv import load_dotenv
from langchain_core.globals import set_debug, set_verbose
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agent.tools import (
    read_file,
    write_file,
    list_files,
    get_current_directory,
    init_project_root,
)

from agent.prompts import *
from agent.states import *

import os
import json
import re


load_dotenv()
set_debug(False)
set_verbose(False)


llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
    max_tokens=4096,
)


def extract_json(content: str) -> str:
    """
    Sometimes LLMs return JSON inside ```json blocks.
    This function cleans that and extracts the JSON object.
    """
    content = content.strip()

    if content.startswith("```"):
        content = re.sub(r"^```json", "", content, flags=re.IGNORECASE).strip()
        content = re.sub(r"^```", "", content).strip()
        content = re.sub(r"```$", "", content).strip()

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in response:\n{content}")

    return content[start:end + 1]


def invoke_json_model(prompt: str, pydantic_model):
    """
    DeepSeek does not reliably support OpenAI json_schema structured output.
    So we ask DeepSeek for normal JSON, then validate it using Pydantic.
    """
    json_llm = llm.bind(
        response_format={"type": "json_object"}
    )

    response = json_llm.invoke(prompt)
    content = response.content

    json_text = extract_json(content)
    data = json.loads(json_text)

    return pydantic_model.model_validate(data)


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]

    resp = invoke_json_model(
        planner_prompt(user_prompt),
        Plan
    )

    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]

    resp = invoke_json_model(
        architect_prompt(plan=plan.model_dump_json()),
        TaskPlan
    )

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan

    print(resp.model_dump_json(indent=2))

    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0
        )

    steps = coder_state.task_plan.implementation_steps

    if coder_state.current_step_idx >= len(steps):
        return {
            "coder_state": coder_state,
            "status": "DONE"
        }

    current_task = steps[coder_state.current_step_idx]

    existing_content = read_file.run(current_task.filepath)

    user_prompt = (
        f"Task: {current_task.task_description}\n\n"
        f"File: {current_task.filepath}\n\n"
        f"Existing content:\n{existing_content}\n\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [
        read_file,
        write_file,
        list_files,
        get_current_directory,
    ]

    react_agent = create_agent(
        model=llm,
        tools=coder_tools,
        system_prompt=coder_system_prompt()
    )

    react_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    })

    coder_state.current_step_idx += 1

    return {
        "coder_state": coder_state
    }


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.set_entry_point("planner")

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {
        "END": END,
        "coder": "coder"
    }
)

agent = graph.compile()


if __name__ == "__main__":
    init_project_root()

    result = agent.invoke(
        {
            "user_prompt": "Build a colourful snake game"
        },
        {
            "recursion_limit": 100
        }
    )

    print("Final State:", result)