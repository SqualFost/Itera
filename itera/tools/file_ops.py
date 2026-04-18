import os

def read_file(path: str) -> str:
    """Read the full content of a file from the given path."""
    with open(path, "r") as f:
        return f.read()

def read_many_files(files: list[str]) -> dict:
    """Read multiple files and return their contents."""
    return {f: open(f).read() for f in files}

def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path."""
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {path}"

def list_files(path: str) -> list:
    """List files and directories in a given path."""
    return os.listdir(path)

def search_files(root: str, query: str) -> list:
    """Search recursively for files matching a query string."""
    matches = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if query.lower() in f.lower():
                matches.append(os.path.join(dirpath, f))
    return matches

def tree(path=".") -> dict:
    """Get a simple directory tree snapshot of a path."""
    return {
        "dirs": [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))],
        "files": [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))],
    }
