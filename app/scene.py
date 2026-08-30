from models import Character, Turn
from personas import list_available_characters, load_character
from ollama_client import chat
import random

def build_messages(character: Character, turns: list[Turn], scene_intro: str, total_turns: int, current_turn: int) -> list[dict]:
    messages = [{"role": "system", "content": character.system_prompt}]
    if not turns and scene_intro:
        messages.append({"role": "user", "content": scene_intro})
    turn_ratio = current_turn/total_turns
    if turn_ratio < .4:
        messages.append({"role": "system", "content": "This is the early part of the plot"})
    elif turn_ratio >= .4 and turn_ratio < .75:
        messages.append({"role": "system", "content": "About halfway through the scene, continue scene development"})
    elif turn_ratio >= .75 and turn_ratio < 1:
        messages.append({"role": "system", "content": "Start working towards a resolution"})
    elif turn_ratio >= 1.0:
        messages.append({"role": "system", "content": "Last turn. Resolve the scene in someway. This can include, but not limited to, conceding a point, agreeing to a compromise, or decisively commit to a course of action, all in ways that are consistent with your personality."})
    for turn in turns:
        if turn.character_id == character.id:
            role = "assistant"
        else:
            role = "user"
        messages.append({"role": role, "content": turn.content})
    # print(messages)
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

async def generate_scene_premise(characters: list[Character]) -> str:
    names = [c.name for c in characters]
    prompt = f"""
    From the available characters, {names}, create a scenario in which these characters will interact with each other. This can
    be, but not limited to, a disagreement, a team meeting, or even in the middle of a battle (them against another enemy). Give them something concrete
    to actually talk about, not limited to but could be: who has the strongest Persona, who will the Phantom Thieves target next, the battle strategy, etc.
    Keep the length of the scenario premise to around 4 sentences at most, but no less than 2. Reply with only the scenario and nothing else.
    """

    messages = [{"role": "user", "content": prompt}]
    reply = await chat("gemma4:e4b", messages)
    return reply.strip()

async def pick_next_speaker(characters: list[Character], turns: list[Turn], total_turns: int, current_turn: int) -> Character:
    ids = [c.id for c in characters]
    lines = []
    for character in characters:
        lines.append(f"{character.id}: {character.summary}")
    id_summary = "\n".join(lines)
    transcript = build_transcript(turns)
    
    director_prompt = f"""You are a scene director. Based on the conversation and their character summaries, decide who should speak next.
    When choosing who speaks next, prioritize in this order:
    1. Someone directly addressed, challenged, or mentioned by name in the last line.
    2. Someone who would naturally react given the flow of conversation, even if not named.
    Consider giving a quieter character a turn after 4 turns of no speaking, but do not force this if it would feel unnatural.
    Follow a natural plot structure with a clearly defined beginning, middle, and end (where the plot has a definitive conclusion/outcome) based on the total number of turns
    and what turn it currently is
    Total turns: {total_turns}
    Current turn number: {current_turn}
    Available characters: {ids}
    Character summaries: {id_summary}
    Transcript so far:
    {transcript}

    Respond with ONLY the character's id, nothing else."""
    
    messages = [{"role": "user", "content": director_prompt}]
    reply = await chat("gemma4:e4b", messages)
    # print(reply)
    chosen = reply.lower().strip()
    if chosen in ids:
        return load_character(chosen)
    else:
        return load_character(random.choice(ids))

