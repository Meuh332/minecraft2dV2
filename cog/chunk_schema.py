from cog.functions import Functions
from cog.server_settings import ServerSettings
server_settings = ServerSettings()


class ChunkSchema:
    def __init__(self, seed, coordinate):
        self.functions = Functions(seed)
        self.seed = seed
        self.coordinate = coordinate
        self.schema = []
        i = 0
        stone_iteration = self.functions.generate(min_hight=server_settings.world_gen_settings["plain"]["stone_height"], max_hight=server_settings.world_gen_settings["plain"]["grass_height"], chunk=coordinate,
                                             scale=server_settings.world_gen_settings["plain"]["scale"], seed=seed)
        for grass_iteration in self.functions.generate(min_hight=server_settings.world_gen_settings["plain"]["grass_height"], max_hight=server_settings.world_gen_settings["plain"]["grass_height"] + server_settings.world_gen_settings["plain"]["height"] // 4 * 3,
                                                  chunk=coordinate, scale=server_settings.world_gen_settings["plain"]["scale"], seed=seed + 1):
            self.schema.append([stone_iteration[i],
                            grass_iteration if grass_iteration - stone_iteration[i] > 1 else stone_iteration[i] + 2])
            # print([stone_iteration[i], grass_iteration])
            i += 1

