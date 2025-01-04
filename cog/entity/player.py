from cog.classes.entity import Entity
from cog.basic_settings import player_size
import pygame


class Player(Entity):
    def __init__(self, coos):
        super().__init__("player", 20, 20, coos, [0, 0], 0, 10, player_size, {}, lambda: None, lambda: None, lambda: None)

    def draw(self, screen, fast_entity_images, camera):
        if not f"{self.type}_{self.state}" in fast_entity_images:
            entity_front_image = pygame.image.load(f"../textures/entity/{self.type}/images/front-s{self.state}.png")
            entity_front_image = pygame.transform.scale(entity_front_image, self.size)
            fast_entity_images[f"{self.type}_{self.state}"] = entity_front_image
        else:
            entity_front_image = fast_entity_images[f"{self.type}_{self.state}"]
        screen.blit(entity_front_image, (self.coos[0], self.coos[1]))
        image_rect = entity_front_image.get_rect()
        image_rect.x = self.coos[0]
        image_rect.y = self.coos[1]
        return fast_entity_images, image_rect
