import pathlib
import subprocess
from typing import Tuple, Optional

from langchain_core.tools import tool


PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


def safe_path_for_project(path: Optional[str] = ".") -> pathlib.Path:
    """
    Safely resolve a path inside PROJECT_ROOT.

    Allows:
    - "."
    - ""
    - "index.html"
    - "folder/file.py"
    - absolute path if it is already inside PROJECT_ROOT

    Blocks:
    - "../outside.txt"
    - any absolute path outside generated_project
    """

    root = PROJECT_ROOT.resolve()

    if path is None or str(path).strip() == "":
        return root

    raw_path = pathlib.Path(str(path))

    if raw_path.is_absolute():
        final_path = raw_path.resolve()
    else:
        final_path = (root / raw_path).resolve()

    try:
        final_path.relative_to(root)
    except ValueError:
        raise ValueError(
            f"Attempt to access outside project root.\n"
            f"Project root: {root}\n"
            f"Requested path: {final_path}"
        )

    return final_path


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"WROTE: {p}"


@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)

    if not p.exists():
        return ""

    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """Returns the generated project root directory."""
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT.resolve())


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)

    if not p.exists():
        return "No files found."

    if not p.is_dir():
        return f"ERROR: {p} is not a directory"

    files = [
        str(f.relative_to(PROJECT_ROOT.resolve()))
        for f in p.glob("**/*")
        if f.is_file()
    ]

    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command inside the project root and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT.resolve()

    res = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout
    )

    return res.returncode, res.stdout, res.stderr


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT.resolve())