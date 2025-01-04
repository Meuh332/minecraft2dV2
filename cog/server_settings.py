import json

class ServerSettings:
    def __init__(self):
        with open("../server_data/world_gen.json", encoding="utf-8") as world_gen_settings:
            self.world_gen_settings = json.load(world_gen_settings)
