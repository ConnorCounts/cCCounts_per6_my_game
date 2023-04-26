# By Connor Counts

"""
Game structure:
GOALS; RULES; FEEDBACK; FREEDOM

My new goal is:
After being very unsucessful with trying to make a platform that has its side be solid, I had to change my goal.
My new goal was to make a game where when the player touches the platform, the platform changes color.
Along with, when the player is no longer touching the platform, the platform goes back to its original color. 
"""


# import libraries
import pygame as pg
import os
# allowing the  Setting and Sprites files to be used
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
    
    # starting a new game
    def new(self):

        # setting up classes to self.__ to be used easier in the code
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)

            #self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (50,50,50), "normal")
            #self.all_sprites.add(self.plat1)
            #self.platforms.add(self.plat1)

        #adding the platforms to the game 
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        
        self.run()

    # while the game is going on events, update, and draw are running too
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # When the user quits the game, the game will sop running and when the user clicks the space bar, the player will jump
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

            # checking to see if the player has collided with a platform
            # if the player hits a platform, the color of the platform will change to red
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                print ("landed!!!!")
                hits[0].image.fill(RED)
            else:
                # if the player is not on a platform, the platform will go back to white
                self.player.standing = False
                    #self.platforms[0].image.fill(WHITE)
                for platform in self.platforms:
                    platform.image.fill(WHITE)

    # Making the screen blue
    def draw (self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # Making paramaters for allowing text to be drawn on the screen
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