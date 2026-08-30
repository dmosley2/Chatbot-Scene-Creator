import json
from pathlib import Path
from models import Character

def load_character(name: str) -> Character:
    filepath = load_persona_dir() / f"{name}.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    return Character(**data)

def load_persona_dir() -> Path:
    return Path(__file__).parent.parent / "personas"

def get_portrait_path(character: Character) -> Path:
    return load_persona_dir() / "images" / character.portrait

def list_available_characters() -> list[Character]:
    characters_list = []
    folder = load_persona_dir()
    characters = folder.glob("*.json")
    for character in characters:
        characters_list.append(load_character(character.stem))
    return characters_list
    