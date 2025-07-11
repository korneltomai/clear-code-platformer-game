from settings import *
from sprites import AnimatedSprite, Bullet
from custom_timer import Timer

class Player(AnimatedSprite):
    def __init__(self, groups, collision_sprites, frames, pos, create_bullet):
        super().__init__(groups, frames, pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        # movement
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.jump_height = 20
        self.on_ground = False
        self.flipped = False

        # shooting
        self.shoot_timer = Timer(500)
        self.create_bullet = create_bullet
        
    def update(self, delta_time):
        self.shoot_timer.update()
        self.check_ground()
        self.handle_input()
        self.move(delta_time)
        self.animate(delta_time)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.direction.y = - self.jump_height

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flipped else 1)
            self.shoot_timer.activate()

    def move(self, delta_time):
        # horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.check_collision("horiontal")

        # vertical
        self.direction.y += self.gravity * delta_time
        self.hitbox_rect.y +=  self.direction.y
        self.check_collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def check_ground(self):
        bottom_rect = pygame.FRect((0,0), (self.hitbox_rect.width - 10, 2)).move_to(midtop = self.hitbox_rect.midbottom)
        self.on_ground = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False

    def check_collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horiontal":
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def animate(self, delta_time):
        if self.direction.x:
            self.frame_index += self.animation_speed * delta_time
            self.flipped = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_ground else self.frame_index

        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flipped, False)