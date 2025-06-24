from settings import * 
from sprites import *
from player import *
from groups import *
from support import *

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

        self.load_assets()
        self.load_map()

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)

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

        self.bee_frames = import_folder("images", "enemies", "bee")
        self.worm_frames = import_folder("images", "enemies", "worm")

        # sounds
        self.audio = import_sounds("audio")

    def load_map(self):
        map = load_pygame(join("data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Main").tiles():
            Sprite((self.all_sprites, self.collision_sprites), image, (x * TILE_SIZE, y * TILE_SIZE))

        for x, y, image in map.get_layer_by_name("Decoration").tiles():
            Sprite((self.all_sprites), image, (x * TILE_SIZE, y * TILE_SIZE))

        for marker in map.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player(self.all_sprites, self.collision_sprites, self.player_frames, (marker.x, marker.y))
            if marker.name == "Worm":
                Worm(self.all_sprites, self.worm_frames, (marker.x, marker.y))

if __name__ == '__main__':
    game = Game()
    game.run() 