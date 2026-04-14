from ollama import chat
import ollama
from tools import (
    read_file,
    read_many_files,
    write_file,
    list_files,
    system_info,
    run_command,
    search_files,
    tree
)

available_functions = {
    "read_file": read_file,
    "read_many_files": read_many_files,
    "write_file": write_file,
    "list_files": list_files,
    "system_info": system_info,
    "run_command": run_command,
    "search_files": search_files,
    "tree": tree,
}

model = 'gemma4:e4b'

#List all availables models
def list_models():
    p = []
    try:
        for m in ollama.list()['models']:
            p.append(m['model'])
        return p
    except Exception:
        return None

#Chat with LLM, takes in argument the model that has been chosen, and the user input
def model_chat(text: str, model: str):
    messages = [
        {
            "role" : "system",
            "content": (
                "You are ITERA, a CLI coding agent."
                "You can use tools when needed."
            )
        },
        {"role": "user", "content": text}
    ]
    while True:
        response = chat(
            model=model,
            messages=messages,
            tools=list(available_functions.values()),
        )

        messages.append(response.message)

        if response.message.tool_calls:
            for call in response.message.tool_calls:
                fn_name = call.function.name
                args = call.function.arguments

                if fn_name in available_functions:
                    result = available_functions[fn_name](**args)
                else:
                    result = "Unknown tool"

                messages.append({
                    "role": "tool",
                    "tool_name": fn_name,
                    "content": str(result)
                })
        else:
            return response.message.content

def change_model(model: str, index: int) -> str:
    models = list_models()
    if not models:
        return model
    if index < 0 or index >= len(models):
        return model
    return models[index]

if __name__ == "__main__":
    model_chat("j'ai combien de ram ? ", model)