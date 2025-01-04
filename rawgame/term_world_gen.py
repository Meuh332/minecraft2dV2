from cog.functions import Functions
from cog.chunk_schema import ChunkSchema
from cog.chunk import Chunk
from colorama import Fore

seed = int(input("seed:"))
functions = Functions(seed=seed)

grid = ChunkSchema(seed, 0)

chunk = Chunk.load_from_schema(seed, grid.schema, grid.coordinate)
last_y = 0
for index in range(len(chunk.chunk_content)):
    block = chunk.chunk_content[len(chunk.chunk_content) - (index + 1)]
    y, x = functions.ic_convert(index)
    if not y == last_y:
        print()
    last_y = y

    block_type = block["type"]
    if block_type == "stone":
        print(Fore.WHITE + "█", end="")
    elif block_type == "air":
        print(Fore.BLUE + "█", end="")
    elif block_type == "grass_block":
        print(Fore.GREEN + "█", end="")
    elif block_type == "dirt":
        print(Fore.LIGHTGREEN_EX + "█", end="")
