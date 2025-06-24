from settings import *
from custom_timer import Timer

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, groups, surf, pos, direction):
        super().__init__(groups, surf, pos)

        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # movement
        self.direction = direction
        self.speed = 850

    def update(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

    
class Fire(Sprite):
    def __init__(self, groups, surf, pos, player):
        super().__init__(groups, surf, pos)
        self.player = player
        self.timer = Timer(150, self.kill, False, True)
        self.flipped = player.flipped
        self.y_offset = pygame.Vector2(0, 9)

        if self.player.flipped:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, _):
        self.timer.update()

        if self.player.flipped:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flipped != self.player.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = not self.flipped


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