from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprites, pos):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        # movement
        self.direction = pygame.math.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.jump_height = 20
        self.on_ground = False
        
    def update(self, delta_time):
        self.check_ground()
        self.handle_input()
        self.move(delta_time)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.direction.y = - self.jump_height

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