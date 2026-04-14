from ollama import chat
import ollama

for m in ollama.list()['models']:
    print(m['model'])

