from dataclasses import dataclass, field

@dataclass
class Character:
    id: str
    name: str
    system_prompt: str
    model: str
    portrait: str
    summary: str

@dataclass
class Turn:
    character_id: str
    content: str