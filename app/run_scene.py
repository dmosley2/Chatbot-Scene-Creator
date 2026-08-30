import asyncio
from models import Character, Turn
from scene import build_messages, pick_character_count, pick_random_characters, pick_next_speaker, generate_scene_premise
from ollama_client import chat
from personas import load_character, get_portrait_path, list_available_characters

async def run_scene():
    total_turns = 10
    count = pick_character_count()
    characters = pick_random_characters(count)
    lookup = {c.id: c for c in characters}

    # print(characters)
    # print(len(characters))

    scene_intro = await generate_scene_premise(characters)
    turns: list[Turn] = []

    print(scene_intro)

    for i in range(total_turns):
        speaker = await pick_next_speaker(characters, turns, total_turns, i+1)
        messages = build_messages(speaker, turns, scene_intro, total_turns, i+1)
        reply = await chat(speaker.model, messages)
        print(f"{speaker.name}: {reply}")
        turns.append(Turn(speaker.id, reply))

asyncio.run(run_scene())