import ollama
from rich.console import Console
from .tools.file_ops import read_file, read_many_files, write_file, list_files, search_files, tree
from .tools.system import system_info, run_command
from .tools.network import check_network, web_search_and_read
from .tools.environmental import get_place_infos

console = Console()
conversation_history = []

available_functions = {
    "read_file": read_file,
    "read_many_files": read_many_files,
    "write_file": write_file,
    "list_files": list_files,
    "system_info": system_info,
    "run_command": run_command,
    "search_files": search_files,
    "tree": tree,
    "check_network": check_network,
    "web_search_and_read": web_search_and_read,
    "get_place_infos": get_place_infos,
}

model_name = 'gemma4:e4b'

def list_models():
    try:
        return [m['model'] for m in ollama.list()['models']]
    except Exception:
        return None

def model_chat(text: str, model: str):
    global conversation_history

    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": (
                "You are ITERA, a CLI coding agent.\n"
                "You MUST follow this process:\n"
                "1. First, create a step-by-step plan.\n"
                "2. Then execute steps one by one using tools if needed.\n"
                "3. After each tool result, update your plan.\n"
                "4. Only stop when the task is fully completed.\n"
                "5. If the task is not finished, continue automatically.\n"
            )
        })

    conversation_history.append({"role": "user", "content": text})

    while True:
        response = ollama.chat(
            model=model,
            messages=conversation_history,
            tools=[
                {"type": "function", "function": {"name": "read_file", "description": read_file.__doc__ or "", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
                {"type": "function", "function": {"name": "read_many_files", "description": read_many_files.__doc__ or "", "parameters": {"type": "object", "properties": {"files": {"type": "array", "items": {"type": "string"}}}, "required": ["files"]}}},
                {"type": "function", "function": {"name": "write_file", "description": write_file.__doc__ or "", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
                {"type": "function", "function": {"name": "list_files", "description": list_files.__doc__ or "", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
                {"type": "function", "function": {"name": "system_info", "description": system_info.__doc__ or "", "parameters": {"type": "object", "properties": {}, "required": []}}},
                {"type": "function", "function": {"name": "run_command", "description": run_command.__doc__ or "", "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]}}},
                {"type": "function", "function": {"name": "search_files", "description": search_files.__doc__ or "", "parameters": {"type": "object", "properties": {"root": {"type": "string"}, "query": {"type": "string"}}, "required": ["root", "query"]}}},
                {"type": "function", "function": {"name": "tree", "description": tree.__doc__ or "", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
                {"type": "function", "function": {"name": "check_network", "description": check_network.__doc__ or "", "parameters": {"type": "object", "properties": {"url": {"type": "string"}, "timeout": {"type": "integer"}}, "required": []}}},
                {"type": "function", "function": {"name": "get_place_infos", "description": get_place_infos.__doc__ or "", "parameters": {"type": "object", "properties": {"lat": {"type": "number"}, "lon": {"type": "number"}}, "required": ["lat", "lon"]}}},
                {"type": "function", "function": {"name": "web_search_and_read", "description": web_search_and_read.__doc__ or "", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "max_pages": {"type": "integer"}}, "required": ["query"]}}}
            ],
        )

        conversation_history.append(response.message)

        if response.message.tool_calls:
            for call in response.message.tool_calls:
                fn_name = call.function.name
                args = call.function.arguments

                values_str = str(list(args.values()))
                max_len = 20
                if len(values_str) > max_len:
                    values_str = values_str[:max_len] + "..."

                console.print(f"❢ Now using tool : {fn_name} on {values_str}")
                result = safe_execute(fn_name, args)

                conversation_history.append({
                    "role": "tool",
                    "tool_name": fn_name,
                    "content": str(result)
                })
        else:
            return response.message.content

def reset_context():
    global conversation_history
    conversation_history = []
    console.print("Conversation history reset successfully")

def safe_execute(fn_name, args):
    fn = available_functions.get(fn_name)
    if not fn:
        return f"[ERROR] Unknown tool: {fn_name}"
    try:
        return fn(**args)
    except Exception as e:
        return f"[ERROR] Tool execution failed: {e}"
