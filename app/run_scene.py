import asyncio
from models import Character, Turn
from scene import build_messages, pick_character_count, pick_random_characters, pick_next_speaker
from ollama_client import chat
from personas import load_character, get_portrait_path, list_available_characters

async def run_scene():
    total_turns = 7
    count = pick_character_count()
    characters = pick_random_characters(3)
    lookup = {c.id: c for c in characters}

    print(characters)
    print(len(characters))

    scene_intro = "Who has the best persona? Start the debate."
    turns: list[Turn] = []

    for i in range(total_turns):
        speaker = await pick_next_speaker(characters, turns)
        messages = build_messages(speaker, turns, scene_intro)
        reply = await chat(speaker.model, messages)
        print(f"{speaker.name}: {reply}")
        turns.append(Turn(speaker.id, reply))

asyncio.run(run_scene())