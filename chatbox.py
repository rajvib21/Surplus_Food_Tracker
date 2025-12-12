import requests

def ask_ollama(prompt, model="llama3.2"):
    url = "http://localhost:11434/api/generate"
    
    res = requests.post(url, json={
        "model": model,
        "prompt": prompt
    }, stream=True)

    output = ""
    for line in res.iter_lines():
        if line:
            output += line.decode() + "\n"
    return output
