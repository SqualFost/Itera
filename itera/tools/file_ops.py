import os

def read_file(path: str) -> str:
    """Read the full content of a file from the given path."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

def read_many_files(files: list[str]) -> dict:
    """Read multiple files and return their contents."""
    result = {}
    for f in files:
        try:
            result[f] = read_file(f)
        except Exception as e:
            result[f] = f"Error: {str(e)}"
    return result

def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path."""
    try:
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written: {path}"
    except Exception as e:
        return f"Error: {str(e)}"

def list_files(path: str) -> dict:
    """List files and directories in a given path."""
    try:
        return {
            "dirs": [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))],
            "files": [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        }
    except Exception as e:
        return {"error": str(e)}

def search_files(root: str, query: str) -> dict:
    """Search recursively for files matching a query string."""
    matches = []
    try:
        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if query.lower() in f.lower():
                    matches.append(os.path.join(dirpath, f))
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e)}

def tree(path=".") -> dict:
    """Get a simple directory tree snapshot of a path."""
    try:
        return {
            "dirs": [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))],
            "files": [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))],
        }
    except Exception as e:
        return {"error": str(e)}
