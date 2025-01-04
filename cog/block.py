from cog.basic_settings import chunk_size
from pygame import Rect

class Block:
    def __init__(self, block_data, chunk_coos, local_block_coos):
        self.block_data = block_data
        self.chunk_coos = chunk_coos
        self.local_block_coos = local_block_coos
        self.static = block_data["static"]
        self.type = block_data["type"]

    @property
    def coos(self):
        return self.chunk_coos * chunk_size + (chunk_size - self.local_block_coos[1] - 1), self.local_block_coos[0] + 1
