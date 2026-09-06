import httpx

async def chat(model: str, messages: list[dict]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model":model,
                "messages": messages,
                "stream":False
            },
            timeout = 60.0
        )
        data = response.json()
        return data["message"]["content"]

async def warmup(model: str) -> None:
    await chat(model, [{"role": "user", "message": "hi"}])
        