def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


# Tools for the LLM to use

def read_file(path: str) -> str:
    """
    Read the full content of a file from the given path.

    Args:
        path (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    with open(path, "r") as f:
        return f.read()

def read_many_files(files: list[str]) -> dict:
    """
    Read multiple files and return their contents.

    Args:
        files (list[str]): List of file paths.

    Returns:
        dict: Mapping of file path to file content.
    """
    return {f: open(f).read() for f in files}

def write_file(path: str, content: str) -> str:
    """
    Write content to a file at the given path.

    Args:
        path (str): File path.
        content (str): Content to write.

    Returns:
        str: Status message.
    """
    with open(path, "w") as f:
        f.write(content)
    return "File written successfully"

def list_files(path: str) -> list:
    """
    List files and directories in a given path.

    Args:
        path (str): Directory path.

    Returns:
        list: List of filenames in the directory.
    """
    import os
    return os.listdir(path)

def system_info() -> dict:
    """
    Retrieve detailed system information.

    Includes:
    - CPU logical/physical cores and usage
    - RAM usage and total memory
    - Disk usage (total/used/free)
    - Battery status if available

    Returns:
        dict: System metrics snapshot.
    """
    import psutil
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "cpu": {
            "logical": psutil.cpu_count(logical=True),
            "physical": psutil.cpu_count(logical=False),
            "usage_percent": psutil.cpu_percent(interval=1),
        },
        "ram": {
            "usage_percent": ram.percent,
            "total_gb": bytes_to_gb(ram.total),
        },
        "disk": {
            "usage_percent": disk.percent,
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
        },
        "battery": (
            {
                "percent": psutil.sensors_battery().percent,
                "charging": psutil.sensors_battery().power_plugged,
            }
            if psutil.sensors_battery()
            else None
        ),
    }


def run_command(cmd: str) -> str:
    """
    Execute a shell command and return its output.

    Args:
        cmd (str): Shell command to execute.

    Returns:
        str: Combined stdout and stderr output.
    """
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def search_files(root: str, query: str) -> list:
    """
    Search recursively for files matching a query string in their filename.

    Args:
        root (str): Root directory to search in.
        query (str): Search keyword.

    Returns:
        list: List of matching file paths.
    """
    import os
    matches = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if query.lower() in f.lower():
                matches.append(os.path.join(dirpath, f))
    return matches

def tree(path=".") -> dict:
    """
    Get a simple directory tree snapshot of a path.

    Args:
        path (str): Directory path.

    Returns:
        dict: Contains lists of directories and files.
    """
    import os
    return {
        "dirs": [d for d in os.listdir(path) if os.path.isdir(d)],
        "files": [f for f in os.listdir(path) if os.path.isfile(f)],
    }



available_tools = [
    "read_file",
    "read_many_files",
    "write_file",
    "list_files",
    "system_info",
    "run_command",
    "search_files",
    "tree",
]