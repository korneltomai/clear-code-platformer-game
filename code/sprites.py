from settings import *
from custom_timer import Timer
from math import sin
from random import randint

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

class Enemy(AnimatedSprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups, frames, pos)
        self.death_timer = Timer(200, self.kill)

    def update(self, delta_time):
        self.death_timer.update()
        if not self.death_timer:
            self.move(delta_time)
            self.animate(delta_time)
            self.check_constraints()

    def destroy(self):
        self.death_timer.activate()
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")

class Bee(Enemy):
    def __init__(self, groups, bee_sprites, player, frames, pos):
        super().__init__(groups, frames["normal"], pos)
        self.bee_sprites = bee_sprites
        self.frames = frames
        self.player = player
        self.speed = randint(250, 450)
        self.amplitude = randint(400, 500)
        self.frequency = randint(300, 600)
        self.direction = pygame.Vector2(-1, 0)

        self.aggressive = False
        self.aggro_range = 400

    def move(self, delta_time):
        if self.aggressive:
            self.direction = (pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center))
        else:
            self.direction.y = sin(pygame.time.get_ticks() / self.frequency)

        self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed * delta_time

    def check_constraints(self):
        if self.rect.right <= 0:
            self.kill()

    def destroy(self):
        for bee in self.bee_sprites:
            if (pygame.Vector2(bee.rect.center) - pygame.Vector2(self.rect.center)).length() < self.aggro_range:
                bee.aggressive = True
        super().destroy()

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        if self.aggressive:
            self.image = self.frames["aggressive"][int(self.frame_index) % len(self.frames)]
        else:
            self.image = self.frames["normal"][int(self.frame_index) % len(self.frames)]

class Worm(Enemy):
    def __init__(self, groups, frames, area_rect):
        super().__init__(groups, frames, area_rect.topleft)
        self.rect.bottomleft = area_rect.bottomleft
        self.area_rect = area_rect  
        
        self.direction = 1
        self.speed = randint(125, 175)

    def move(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

    def check_constraints(self):
        if not self.area_rect.contains(self.rect):
            self.direction = -self.direction
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
            