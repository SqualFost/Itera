from ollama import chat
import ollama


#List all availables models
def list_models():
    p = []
    try:
        for m in ollama.list()['models']:
            p.append(m['model'])
        return p
    except Exception:
        return []

#Chat with LLM, takes in argument the model that has been chosen, and the user input
def model_chat(text: str, model: str):
    stream = chat(
        model=model,
        messages=[{'role': 'user', 'content': f"{text}"}],
        stream=True,
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

print(list_models())

model_chat('salut ca va ?', 'gemma4:e4b')