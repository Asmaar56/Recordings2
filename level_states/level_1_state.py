# import libraries
import pygame

# import parent class
from IAppState import IAppState

# import elements and events
from pygame_gui import UIManager
from pygame import KEYDOWN

# import camera
from camera import Camera

# import player
from player import Player

from object_1 import Object1


class Level1State(IAppState):  # class inherits from IAppState

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: pygame.Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # variables
        self.camera = None
        self.player = None
        self.object_1 = None

        # level variables
        self.player = None
        self.tile_list = []
        self.tile_size = 50
        self.block_img = pygame.image.load('level_states/game_images/block.png')

        self.all_sprites = None  # images

        # level information
        self.level_data = [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = pygame.Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # make camera
        world_centre = pygame.Vector2(self.window_size)
        self.camera = Camera(world_centre, pygame.Rect((0, 0), self.window_size))

        # create sprite groups
        self.all_sprites = pygame.sprite.Group()

        # create player
        player_position = (self.window_surface.get_rect().centerx,
                           self.window_surface.get_rect().bottom - 50)
        player_image = pygame.image.load('level_states/game_images/gunman_2.png')
        player_bullet_image = pygame.image.load('level_states/game_images/laser.jpg')
        self.player = Player(image=player_image,
                             bullet_image=player_bullet_image,
                             position=player_position,
                             all_sprites_group=self.all_sprites)

        # create objects
        object_1_position = (self.window_surface.get_rect().centerx + 100,
                             self.window_surface.get_rect().bottom - 100)

        self.object_1 = Object1(object_1_position)
        self.make_level()

    def make_level(self):  # build the level by adding images on the screen
        row_counter = 0
        for row in self.level_data:
            column_counter = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(self.block_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_counter * self.tile_size
                    img_rect.y = row_counter * self.tile_size
                    view_pos_rect = img_rect.copy()
                    tile = (img, img_rect, view_pos_rect)
                    self.tile_list.append(tile)
                column_counter += 1
            row_counter += 1

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        if self.player is not None: # kill player
            self.player.kill()
            self.player = None

        if self.all_sprites is not None: # clear sprite group
            self.all_sprites.empty()
            self.all_sprites = None

        self.camera = None  # kill camera
        self.tile_list = None  # clear tiles

    def process_event(self, event: pygame.event.Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events
        self.player.process_event(event)

        if event.type == KEYDOWN:  # if any keyboard key is pressed
            if event.key == pygame.K_p:  # return to menu
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('KEY P pressed in LEVEL1STATE')

    def update(self, time_delta: float):  # update takes time as parameter
        self.camera.update(time_delta, self.player.position)
        self.player.update(time_delta, self.camera)
        self.all_sprites.update(time_delta, self.camera)
        for tile in self.tile_list:  # draw level
            tile[2].x = tile[1].x - self.camera.viewport_rect.left
            tile[2].y = tile[1].y - self.camera.viewport_rect.top
        self.object_1.update(time_delta)
        self.ui_manager.update(time_delta=time_delta)

    def draw(self):  # draw changes onto window
        self.window_surface.blit(self.background_surface, (0, 0))

        for tile in self.tile_list:  # draw level
            self.window_surface.blit(tile[0], tile[2])

        self.all_sprites.draw(self.window_surface)
        self.ui_manager.draw_ui(self.window_surface)  # draws ui elements onto window
        #self.player.draw(self.window_surface)
        self.object_1.draw(self.window_surface)