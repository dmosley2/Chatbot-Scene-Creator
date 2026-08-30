from models import Character, Turn
from personas import list_available_characters, load_character
from ollama_client import chat
import random

def build_messages(character: Character, turns: list[Turn], scene_intro: str | None = None) -> list[dict]:
    messages = [{"role": "system", "content": character.system_prompt}]
    if not turns and scene_intro:
        messages.append({"role": "user", "content": scene_intro})
    for turn in turns:
        if turn.character_id == character.id:
            role = "assistant"
        else:
            role = "user"
        messages.append({"role": role, "content": turn.content})
    return messages

def pick_character_count(min: int = 2, max: int = 3) -> int:
    return random.randint(min, max)

def pick_random_characters(k: int) -> list[Character]:
    available = list_available_characters()
    return random.sample(available, min(len(available), k))

def build_transcript(turns: list[Turn]) -> str:
    lines = []
    for turn in turns:
        lines.append(f"{turn.character_id}: {turn.content}")
    return "\n".join(lines)

async def pick_next_speaker(characters: list[Character], turns: list[Turn]) -> Character:
    ids = [c.id for c in characters]
    transcript = build_transcript(turns)
    
    director_prompt = f"""You are a scene director. Based on the conversation, decide who should speak next.
    When choosing who speaks next, consider:
    - If someone was directly addressed, challenged, or mentioned by name, they likely respond next.
    - Avoid letting the same character dominate several turns in a row.
    - Characters who haven't spoken yet should get a chance eventually.
    Available characters: {ids}
    Transcript so far:
    {transcript}

    Respond with ONLY the character's id, nothing else."""
    
    messages = [{"role": "user", "content": director_prompt}]
    reply = await chat("gemma4:e4b", messages)
    print(reply)
    chosen = reply.lower().strip()
    if chosen in ids:
        return load_character(chosen)
    else:
        return load_character(random.choice(ids, 1))

