import argparse
import sys
import traceback

from agent.graph import agent
from agent.tools import init_project_root


def main():
    parser = argparse.ArgumentParser(
        description="Run the engineering project planner."
    )

    parser.add_argument(
        "--recursion-limit",
        "-r",
        type=int,
        default=100,
        help="Set the recursion limit for the planner."
    )

    args = parser.parse_args()

    try:
        init_project_root()

        user_prompt = input("What is your engineering project? ")

        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )

        print("Final State:", result)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)

    except Exception as e:
        print("\nAn error occurred:", str(e), file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()