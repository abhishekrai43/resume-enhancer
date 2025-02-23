import requests

ollama_url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
data = {
    "model": "mistral",
    "prompt": "Hello, how are you?",
    "stream": False
}

response = requests.post(ollama_url, json=data, headers=headers)
print(response.json())
