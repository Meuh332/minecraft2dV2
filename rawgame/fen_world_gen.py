from collections import deque
import pygame
from cog.functions import Functions
from cog.basic_settings import *
import time
from cog.entity.player import Player
from cog.main_objects import camera, keyboard, instant_keyboard
import cog.fasts as fasts
from cog.chunk import Chunk
import math
pygame.init()


screen = pygame.display.set_mode((1080, 500))
screen_width = screen.get_width()
pygame.display.set_caption("minecraft 2D")


save = ""
functions = Functions(seed)
my_font = pygame.font.SysFont('Comic Sans MS', 20)
screen_chunk_split = math.ceil(screen_width / (chunk_size * block_size))


running = True
fps_history = deque(maxlen=50)
pos = (0, 0)
entity_list = []


player = Player([functions.x_by_x_co(16), functions.y_by_y_co(35)])
entity_list.append(player)
fps_text_surface = my_font.render('FPS', False, (0, 0, 0))
while running:
    start = time.time()
    screen.fill((135, 206, 235))
    screen.blit(fps_text_surface, (0, 0))
    instant_keyboard.reset()
    for event in pygame.event.get():
        try:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard.press(event.key, event.unicode)
                instant_keyboard.press(event.key, event.unicode)
            elif event.type == pygame.KEYUP:
                keyboard.release(event.key)
            pos = event.pos
        except:
            pass

    if keyboard.pressed("a"):
        player.momentum[0] = min(player_speed * -1, player.momentum[0] * -1)

    if keyboard.pressed("d"):
        player.momentum[0] = max(player_speed, player.momentum[0])

    if keyboard.pressed(pygame.K_SPACE):
        if player.data["on_the_ground"]:
            player.momentum[1] -= player_jump_momentum

    displayed_chunk = []
    for chunk_step in range(screen_chunk_split):
        current_chunk = Chunk.chunk_by_x(screen_chunk_split * chunk_step, seed, True)
        if not current_chunk.chunk_coos in displayed_chunk:
            current_chunk.draw(screen, (0, chunk_y))
            displayed_chunk.append(current_chunk.chunk_coos)


    fast_entity_images, player_rect = player.draw(screen, fasts.fast_entity_images, camera)
    for entity in entity_list:
        # grav & momentum y
        entity.data["on_the_ground"] = False
        for momentum in range(0, entity.momentum[1], 1 if entity.momentum[1] >= 0 else -1):
            entity.coos[1] += 1 if entity.momentum[1] >= 0 else -1
            entity_bottom = entity.bottom_rect if entity.momentum[1] >= 0 else entity.top_rect
            entity.coos[1] -= 1 if entity.momentum[1] >= 0 else -1
            colliders = []

            bottom_y = math.ceil(entity.size[1] / block_size) if entity.momentum[1] >= 0 else -1
            colliders.append([pygame.Rect(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y), block_size, block_size), functions.get_block_by_xy(Chunk.chunk_by_x(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), seed, True), (functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y)))])
            for step in range(math.ceil(entity.size[0] / block_size)):
                colliders.append([pygame.Rect(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + step), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y), block_size, block_size), functions.get_block_by_xy(Chunk.chunk_by_x(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + step), seed, True), (functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + step), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y)))])

            entity.coos[1] += 1 if entity.momentum[1] >= 0 else -1
            collide = False
            for collider, block in colliders:
                # pygame.draw.rect(screen, 0, pygame.Rect((functions.x_by_x_co(block.coos[0]), functions.y_by_y_co(block.coos[1])), (block_size, block_size)))
                if not block.typed == "air":
                    if entity_bottom.colliderect(collider):
                        collide = True
            if collide:
                entity.data["on_the_ground"] = True
                entity.coos[1] -= 1 if entity.momentum[1] >= 0 else -1
                entity.momentum[1] = 0
                break

        else:
            if not entity.momentum[1] > max_falling_speed:
                entity.momentum[1] += 1

        for momentum in range(0, entity.momentum[0], 1 if entity.momentum[0] >= 0 else -1):
            entity.coos[0] += 1 if entity.momentum[0] >= 0 else -1
            entity_side = entity.right_rect if entity.momentum[0] >= 0 else entity.left_rect
            entity.coos[0] -= 1 if entity.momentum[0] >= 0 else -1
            colliders = []

            side_x = math.ceil(entity.size[0] / block_size) if entity.momentum[0] >= 0 else -1
            colliders.append([pygame.Rect(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y), block_size, block_size), functions.get_block_by_xy(Chunk.chunk_by_x(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), seed, True), (functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) - 1), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - bottom_y)))])
            for step in range(math.ceil(entity.size[0] / block_size) + 1):
                colliders.append([pygame.Rect(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + side_x), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - step), block_size, block_size), functions.get_block_by_xy(Chunk.chunk_by_x(functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + side_x), seed, True), (functions.x_by_x_co(functions.x_co_by_x(entity.coos[0]) + side_x), functions.y_by_y_co(functions.y_co_by_y(entity.coos[1]) - step)))])

            entity.coos[0] += 1 if entity.momentum[0] >= 0 else -1
            collide = False
            for collider, block in colliders:
                pygame.draw.rect(screen, 0, collider)
                pygame.draw.rect(screen, 255, entity_side)
                if not block.type == "air":
                    if entity_side.colliderect(collider):
                        collide = True
            if collide:
                entity.coos[0] -= 1 if entity.momentum[0] >= 0 else -1
                entity.momentum[0] = 0
                break

        else:
            if not entity.momentum[0] == 0:
                entity.momentum[0] -= 1 if entity.momentum[0] >= 0 else -1

    elapsed_time = time.time() - start
    current_fps = 1 / elapsed_time if elapsed_time > 0 else 0
    fps_history.append(current_fps)
    average_fps = sum(fps_history) / len(fps_history)
    fps_text_surface = my_font.render(f"{round(average_fps)} fps", False, (0, 0, 0))
    pygame.display.flip()
    time.sleep(max(0.05 - (time.time() - start), 0))
