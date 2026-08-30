import asyncio
from ollama_client import chat

async def main():
    messages = [
        {"role": "system", "content": "You are a pirate. Keep your answers short."},
        {"role": "user", "content": "What's the weather like today?"}
    ]
    reply = await chat("gemma4:e4b", messages)
    print(reply)

asyncio.run(main())