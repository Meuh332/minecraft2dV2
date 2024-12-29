from noise import pnoise1


class Functions:
    def __init__(self):
        pass

    @staticmethod
    def generate(min_hight=60, max_hight=90, chunk=1, chunk_size=64, scale=0.1, seed=0):
        """Génère une liste de hauteurs pour un chunk donné, avec continuité logique."""
        heights = []
        base_x = chunk * chunk_size  # Position de départ du chunk
        for x in range(chunk_size):
            noise_value = pnoise1((base_x + x) * scale + seed)  # Bruit Perlin à partir de x
            height = int(noise_value * (max_hight - min_hight) / 2 + (max_hight + min_hight) / 2)
            heights.append(height)
        return heights

