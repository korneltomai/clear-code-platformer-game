from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, groups, frames, pos):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        super().__init__(groups, self.frames[self.frame_index], pos)

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Bee(AnimatedSprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups, frames, pos)

    def update(self, delta_time):
        self.animate(delta_time)

class Worm(AnimatedSprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups, frames, pos)

    def update(self, delta_time):
        self.animate(delta_time)