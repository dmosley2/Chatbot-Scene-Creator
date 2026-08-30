from models import Character, Turn
from scene import build_messages

ryuji = Character(id="ryuji", name="Ryuji", system_prompt="You are Ryuji Sakamoto from Persona 5 Royal.", model="gemma4:e4b")
morgana = Character(id="morgana", name="Morgana", system_prompt="You are Morgana from Persona 5 Royal.", model="gemma4:e4b")

turns = [
    Turn(character_id="ryuji", content="Mona, quit actin' like you're the boss of this team."),
    Turn(character_id="morgana", content="I AM the boss! Someone's gotta keep you idiots in line!"),
]

print(build_messages(ryuji, turns))
print(build_messages(morgana, turns))