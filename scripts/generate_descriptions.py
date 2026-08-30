import json
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "app"))
# print(sys.path)
from personas import list_available_characters, load_character, load_persona_dir
from ollama_client import chat
from models import Character

async def generate_description(character: Character):
    prompt = f"""
    Create a short summary of {character.name}'s system prompt.
    This should be a 1 sentence summary that encapsulates the personality described
    in the given prompt. Reply with only the one sentence summary and nothing else.

    Character prompt: {character.system_prompt}
    """
    messages = [{"role": "user", "content": prompt}]
    summary = await chat("gemma4:e4b", messages)
    return summary.strip()

def update_character_description(name: str, description: str) -> None:
    filepath = load_persona_dir() / f"{name}.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    data["summary"] = description
    with open(filepath, "w") as f:
        json.dump(data, f)

async def main():
    characters_list = list_available_characters()
    for character in characters_list:
        summary = await generate_description(character)
        update_character_description(character.id, summary)

if __name__ == "__main__":
    asyncio.run(main())
