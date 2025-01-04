import pygame

class Entity:
    def __init__(self, type, health, total_health, coos, momentum, state, total_states, size, on_spawn, on_death, on_damage):
        self.type = type
        self.heath = health
        self.total_health = total_health
        self.coos = coos
        self.momentum = momentum
        self.state = state
        self.total_states = total_states
        self.size = size
        self.on_death = on_death
        self.on_damage = on_damage
        on_spawn()

    def teleport(self, x, y):
        self.coos = [x, y]

    def kill(self, killer):
        self.state = -1
        self.heath = 0
        self.on_death(self, killer)

    def deal_damage(self, damage, by):
        if self.heath <= damage:
            self.kill(by)
            self.on_damage(damage, by, True)
            return True
        else:
            self.heath -= damage
            if self.heath > self.total_health:
                self.heath = self.total_health
            self.on_damage(damage, by, False)
            return False

    def next_state(self):
        self.state += 1
        if self.state > self.total_states:
            self.state = 1

    def draw(self, screen, fast_entity_images, camera):
        if not f"{self.type}_{self.state}" in fast_entity_images:
            entity_front_image = pygame.image.load(f"../textures/entity/{self.type}/images/front-s{self.state}.png")
            entity_front_image = pygame.transform.scale(entity_front_image, self.size)
            fast_entity_images[f"{self.type}_{self.state}"] = entity_front_image
        else:
            entity_front_image = fast_entity_images[f"{self.type}_{self.state}"]
        screen.blit(entity_front_image, (self.coos[0] + camera.x, self.coos[1] + camera.y))
        return fast_entity_images

    @property
    def bottom_rect(self):
        return pygame.Rect(self.coos[0], self.coos[1] + self.size[1] - 1, self.size[0], 1)

    @property
    def right_rect(self):
        return pygame.Rect(self.coos[0] + self.size[0] - 1, self.coos[1], 1, self.size[1])

    @property
    def left_rect(self):
        return pygame.Rect(self.coos[0], self.coos[1], 1, self.size[1])

    @property
    def top_rect(self):
        return pygame.Rect(self.coos[0], self.coos[1], self.size[0], 1)
