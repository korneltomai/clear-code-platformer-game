from settings import * 
from sprites import *
from player import *
from groups import *
from support import *
from custom_timer import Timer
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bee_sprites = pygame.sprite.Group()

        # timers
        self.bee_timer = Timer(1000, self.create_bee, True, True)

        self.load_assets()
        self.setup()

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.check_collisions()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

    def load_assets(self):
        # graphics
        self.player_frames = import_folder("images", "player")
        self.bullet_surface = import_image("images", "gun", "bullet")
        self.fire_surface = import_image("images", "gun", "fire")

        self.bee_frames = {
            "normal": import_folder("images", "enemies", "bee"),
            "aggressive": import_folder("images", "enemies", "bee_aggro")
        }
        self.worm_frames = import_folder("images", "enemies", "worm")

        # sounds
        self.audio = import_sounds("audio")
        self.audio["music"].set_volume(0.1)
        self.audio["shoot"].set_volume(0.3)
        self.audio["impact"].set_volume(0.3)

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        self.map_width = map.width * TILE_SIZE
        self.map_height = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name("Main").tiles():
            Sprite((self.all_sprites, self.collision_sprites), image, (x * TILE_SIZE, y * TILE_SIZE))

        for x, y, image in map.get_layer_by_name("Decoration").tiles():
            Sprite((self.all_sprites), image, (x * TILE_SIZE, y * TILE_SIZE))

        for marker in map.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player(self.all_sprites, self.collision_sprites, self.player_frames, (marker.x, marker.y), self.create_bullet)
            if marker.name == "Worm":
                Worm((self.all_sprites, self.enemy_sprites), self.worm_frames, pygame.FRect(marker.x, marker.y, marker.width, marker.height))

        self.audio["music"].play(loops = -1)

    def create_bee(self):
        Bee((self.all_sprites, self.enemy_sprites, self.bee_sprites), self.bee_sprites, self.player, self.bee_frames, (self.map_width + WINDOW_WIDTH / 2, randint(0, self.map_height)))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surface.get_width()
        Bullet((self.all_sprites, self.bullet_sprites), self.bullet_surface, (x, pos[1]), direction)
        Fire(self.all_sprites, self.fire_surface, pos, self.player)
        self.audio["shoot"].play()

    def check_collisions(self):
        # bullets -> enemies
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio["impact"].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
                    

        # enemies -> player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

        # player fall
        if self.player.hitbox_rect.centery > self.map_height + 1000:
            self.running = False

if __name__ == '__main__':
    game = Game()
    game.run() 