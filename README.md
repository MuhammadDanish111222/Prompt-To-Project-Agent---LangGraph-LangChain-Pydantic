# Prompt To Project Agent

Prompt To Project Agent is a Python based AI software generation system that converts a simple project idea into a structured plan, breaks it into implementation tasks, and generates project files automatically.

The project uses LangGraph, LangChain, DeepSeek, and Pydantic to build a multi stage agent workflow.

## Overview

This agent takes a user prompt such as:

```text
snake game
```

Then it creates a project plan, prepares implementation steps, and writes the required files inside the `generated_project` folder.

Example output:

```text
generated_project/
├── index.html
├── style.css
└── script.js
```

## Main Features

- Converts natural language project ideas into structured plans
- Breaks project plans into clear engineering tasks
- Uses an AI coding agent to generate files
- Stores generated code inside a safe project directory
- Uses Pydantic models for structured validation
- Uses LangGraph to manage the workflow
- Supports simple frontend project generation
- Includes file safety checks to prevent writing outside the project folder

## How It Works

The project follows a three stage workflow:

```text
User Prompt
    ↓
Planner Agent
    ↓
Architect Agent
    ↓
Coder Agent
    ↓
Generated Project Files
```

## Agent Stages

### Planner Agent

The planner receives the user prompt and creates a structured project plan.

It defines:

- Project name
- Project description
- Tech stack
- Main features
- Required files

### Architect Agent

The architect receives the project plan and converts it into detailed implementation steps.

It defines:

- Which files need to be created
- What each file should contain
- Which functions or variables are required
- How the files should work together
- The correct order of implementation

### Coder Agent

The coder agent receives one implementation step at a time and writes the actual code files.

It uses tools such as:

- `read_file`
- `write_file`
- `list_files`
- `get_current_directory`

All generated files are stored inside:

```text
generated_project/
```

## Tech Stack

| Technology | Purpose |
|----------|---------|
| Python | Main programming language |
| LangGraph | Agent workflow management |
| LangChain | LLM and tool integration |
| DeepSeek | Language model |
| Pydantic | Data validation |
| dotenv | Environment variable loading |
| pathlib | Safe file path handling |

## Project Structure

```text
code_creater_agent/
│
├── main.py
│
├── agent/
│   ├── graph.py
│   ├── prompts.py
│   ├── states.py
│   └── tools.py
│
├── generated_project/
│
├── .env
├── requirements.txt
└── README.md
```

## File Responsibilities

### main.py

This is the entry point of the application.

It is responsible for:

- Reading the user prompt
- Starting the agent workflow
- Passing recursion limit settings
- Printing the final result
- Handling errors and keyboard interruption

### agent/graph.py

This file contains the main agent workflow.

It is responsible for:

- Setting up the language model
- Defining the planner agent
- Defining the architect agent
- Defining the coder agent
- Building the LangGraph workflow
- Running the coder repeatedly until all tasks are complete

### agent/prompts.py

This file stores the prompts used by each agent.

It includes:

- Planner prompt
- Architect prompt
- Coder system prompt

### agent/states.py

This file defines the Pydantic models used in the project.

It includes:

- `File`
- `Plan`
- `ImplementationTask`
- `TaskPlan`
- `CoderState`

These models help keep the output structured and easier to validate.

### agent/tools.py

This file contains the tools used by the coder agent.

It includes:

- Safe path validation
- File reading
- File writing
- File listing
- Project root initialization
- Optional command execution

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/code-creater-agent.git
cd code-creater-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a .env file

Create a `.env` file in the root directory and add your DeepSeek API key:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## Usage

Run the project:

```bash
python main.py
```

Enter a project idea when asked:

```text
What is your engineering project? snake game
```

The agent will then:

1. Create a project plan
2. Convert the plan into implementation steps
3. Generate the required files
4. Save the files inside `generated_project`

## Example

Input:

```text
snake game
```

Possible generated output:

```text
generated_project/
├── index.html
├── style.css
└── script.js
```

The generated project may include:

- HTML structure
- CSS styling
- JavaScript game logic
- Score tracking
- Restart functionality
- Collision detection

## Safety

The project includes path safety logic to make sure the agent only writes files inside the allowed project folder.

Allowed folder:

```text
generated_project/
```

This prevents the agent from accidentally modifying files outside the generated project directory.

## Common Errors

### response_format type is unavailable

This error can happen when the model provider does not support the structured response format requested by LangChain.

A safer solution is to ask the model for plain JSON and then validate that JSON manually with Pydantic.

### Attempt to write outside project root

This means the safety function blocked a path that looked unsafe.

Make sure all generated files are being written inside:

```text
generated_project/
```

### generated_project already exists as a file

This means `generated_project` exists, but it is a file instead of a folder.

Delete it with:

```bash
Remove-Item .\generated_project -Force
```

Then run the project again:

```bash
python main.py
```

## Future Improvements

- Add React project generation
- Add automatic dependency installation
- Add generated project testing
- Add better error recovery
- Add support for multiple LLM providers
- Add Streamlit or FastAPI interface
- Add automatic README generation for generated projects
- Add GitHub repository creation support
- Add support for project templates

## Author

Muhammad Danish Riasat

GitHub: (https://github.com/MuhammadDanish111222)

## License

This project is available for learning and development purposes.
