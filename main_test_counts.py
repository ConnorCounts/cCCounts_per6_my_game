# By Connor Counts
# Agenda:  
# Build file and folder structures
# Create libraries

"""
Game structure:
GOALS; RULES; FEEDBACK; FREEDOM

My goal is:

Is to create a new platform, seperate from the bottom, that does not let me move through it on the x or y axis.
I want player to be stopped when it hits this new platform instead of moving through the other platforms to the top.
Create a solid platform that can still hold the player on top but the player cannot go through the platofrm. 

"""


# import libs
import pygame as pg
import os
# import settings 
from settings_test_counts import *
from sprites_test_counts import *
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# create game class in order to pass properties to the sprite file

class Game: 
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)
    
    def new(self):
        # starting a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        # self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.all_sprites.add(self.plat1)

        self.platforms.add(self.plat1)
        
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(0,10):
            m = Mob(20,20,(0,255,0))
            self.all_sprites.add(m)
            self.enemies.add(m)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        self.all_sprites.update()
        
        # if the player is falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #if abs(self.player.vel.x) > abs(self.player.vel.y):
                    #if self.player.vel.x > 0:
                        #print("Im going faster on the x and coming from the left...")
                self.player.standing = True
                if hits[0].variant == "disappearing":
                    hits[0].kill()
                elif hits[0].variant == "bouncey":
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
            else:
                self.player.standing = False

    def draw (self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        if self.player.standing:
            self.draw_text("I hit a plat!", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
           
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
 
# instantiate the game class
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()