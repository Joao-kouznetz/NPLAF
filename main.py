import ollama

response = ollama.chat(
    model="llama3.1:latest",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)
print(response["message"]["content"])
