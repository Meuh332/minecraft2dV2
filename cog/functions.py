from noise import pnoise1
import random
from cog.basic_settings import chunk_size, block_size, chunk_y
from cog.main_objects import camera


class Functions:
    def __init__(self, seed):
        self.seed = seed

    @staticmethod
    def generate(min_hight=60, max_hight=90, chunk=1, scale=0.1, seed=0):
        """Génère une liste de hauteurs pour un chunk donné, avec continuité logique."""
        heights = []
        base_x = chunk * chunk_size  # Position de départ du chunk
        for x in range(chunk_size):
            noise_value = pnoise1((base_x + x) * scale + seed)  # Bruit Perlin à partir de x
            height = int(noise_value * (max_hight - min_hight) / 2 + (max_hight + min_hight) / 2)
            heights.append(height)
        return heights

    def randint(self, a, b, coos):
        random.seed(self.seed + coos)
        return random.randint(a, b)

    @staticmethod
    def ic_convert(x):
        if type(x) == int:
            return x // chunk_size, x % chunk_size
        else:
            return x[0] * chunk_size + x[1]

    @staticmethod
    def force_index(x):
        if not type(x) == int:
            x = Functions.ic_convert(x)
        return x

    @staticmethod
    def y_co_by_y(y):
        return 100 - abs(chunk_y - (y + camera.y * -1)) // block_size

    @staticmethod
    def x_co_by_x(x):
        return (x + camera.x * -1) // block_size

    @staticmethod
    def x_by_x_co(x):
        return x * block_size + camera.x

    @staticmethod
    def y_by_y_co(y):
        return (chunk_y + 100 * block_size) - y * block_size + camera.y

    def get_block_by_xy(self, chunk, xy):
        x, y = xy
        return chunk.block(
            (self.y_co_by_y(y) - (1 - chunk.chunk_coos)) * chunk_size + (chunk_size - self.x_co_by_x(x) - 1)
        )
