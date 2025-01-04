from cog.basic_settings import chunk_size, load_from_save, block_size
from cog.functions import Functions
from cog.block import Block
import json
import cog.fasts as fast
from cog.chunk_schema import ChunkSchema
import pygame
from cog.main_objects import camera


def image_data(block_name):
    with open(f"../textures/blocks/{block_name}/data.json", "r") as data_file:
        return json.loads(data_file.read())


class Chunk:
    def __init__(self, chunk_data, chunk_coos):
        self.chunk_data = chunk_data
        self.chunk_content = chunk_data.get("chunk_content")
        self.seed = chunk_data.get("seed")
        self.functions = Functions(self.seed)
        self.chunk_coos = chunk_coos

    @staticmethod
    def load_from_schema(seed, schema, chunk_coos):
        functions = Functions(seed)
        chunk_content = []

        saved_statics = {}

        for index in range(functions.ic_convert((99, chunk_size))):
            y, x = functions.ic_convert(index)
            stone_height, grass_height = schema[x]
            block = {}
            if y <= stone_height:
                block["type"] = "stone"
            elif stone_height < y < grass_height:
                block["type"] = "dirt"
            elif y == grass_height:
                block["type"] = "grass_block"
            else:
                block["type"] = "air"

            block["data"] = {}
            if block["type"] in saved_statics:
                block["static"] = saved_statics[block["type"]]
            else:
                block_image_static = image_data(block["type"])["static"]
                block["static"] = block_image_static
                saved_statics[block["type"]] = block_image_static
            chunk_content.append(block)

        chunk_data = {
            "seed": seed,
            "chunk_content": chunk_content
        }
        return Chunk(chunk_data, chunk_coos)

    def block(self, index):
        if type(index) == int:
            index2 = self.functions.ic_convert(index)
            return Block(self.chunk_content[index], self.chunk_coos, index2)

    def draw(self, screen, chunk_pos):
        if not load_from_save:
            for index in range(len(self.chunk_content)):
                block = self.chunk_content[len(self.chunk_content) - (index + 1)]
                y, x = self.functions.ic_convert(index)
                block_type = block["type"]
                if not block_type == "air":
                    if block["static"]:
                        if not block_type in fast.fast_static_image:
                            block_front_image = pygame.image.load(
                                f"../textures/blocks/{block_type}/images/front-s0.png")
                            block_front_image = pygame.transform.scale(block_front_image, (block_size, block_size))
                            fast.fast_static_image[block_type] = block_front_image
                        else:
                            block_front_image = fast.fast_static_image[block_type]
                        screen.blit(block_front_image, (
                        (chunk_pos[0] + x * block_size) + camera.x, (chunk_pos[1] + y * block_size) + camera.y))
                        if block_type == "grass_block":
                            # print(chunk_pos[1] + y * block_size)
                            pass

    @staticmethod
    def chunk_by_x(x, seed, get_object=False):
        chunk_id = (x + camera.x * -1) // (chunk_size * block_size)
        if not get_object:
            return chunk_id
        if not load_from_save:
            if not f"{chunk_id}_{seed}" in fast.fast_chunks:
                chunk_schema = ChunkSchema(seed, chunk_id)
                chunk = Chunk.load_from_schema(seed, chunk_schema.schema, chunk_schema.coordinate)
                if len(fast.fast_chunks) > 50:
                    fast.fast_chunks = {}
                fast.fast_chunks[f"{chunk_id}_{seed}"] = chunk
            else:
                chunk = fast.fast_chunks[f"{chunk_id}_{seed}"]

            return chunk
