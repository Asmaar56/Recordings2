import pygame
import csv

import pygame_gui
from IAppState import IAppState

from player import Player
from camera import Camera
from sheep import Sheep
from coin import Coin

from level_states.level_1_data import level_data


class Level1State(IAppState):

    def __init__(self,
                 window_surface: pygame.Surface,
                 window_size,
                 ui_manager: pygame_gui.UIManager):
        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        self.level = 1  # what level is this

        # inherited variables
        self.window_size = window_size
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.all_sprites = None
        self.player_shots = None
        self.player_collision_group = None

        # background variables
        self.background_texture = None
        self.background_position = (0, 0)

        # area of the world
        self.world_bounds = (1280 * 2.5, 720 * 2.5)

        # entities
        self.player = None
        self.camera = None

        # level variables
        self.tile_list = []
        self.tile_size = 50

        self.level_data = level_data

    def start(self):  # called when state starts up

        self.all_sprites = pygame.sprite.Group()
        self.player_shots = pygame.sprite.Group()
        self.player_collision_group = pygame.sprite.Group()

        # centre of the world is set to size of window
        # so the world is 2x the size of the window
        world_centre = pygame.Vector2(self.window_size)

        # create camera
        self.camera = Camera(world_centre,
                             pygame.Rect((0, 0), self.window_size),
                             pygame.Rect((0, 0), self.world_bounds))

        # create player
        player_texture = pygame.image.load('level_states/game_images/gunman_2.png').convert_alpha()
        self.player = Player(player_texture=player_texture,
                             world_bounds=self.world_bounds,
                             window_surface=self.window_surface,
                             player_shots_group=self.player_shots,
                             player_collision_group=self.player_collision_group,
                             all_sprites_group=self.all_sprites)

        #  background texture for the level
        self.background_texture = pygame.transform.smoothscale(
            pygame.image.load('level_states/game_images/background_image2.png').convert(),
            self.world_bounds)

        self.make_level()

    def make_level(self):
        sheep_texture = pygame.image.load('level_states/game_images/sheep3.png').convert_alpha()
        coin_texture = pygame.image.load('level_states/game_images/coin.png').convert_alpha()

        row_counter = 0
        for row in self.level_data:
            column_counter = 0
            for tile in row:

                if tile == 1:
                    pos_x = column_counter * self.tile_size
                    pos_y = row_counter * self.tile_size

                    self.tile_list.append(Sheep(sheep_texture=sheep_texture,
                                                position=(pos_x, pos_y),
                                                player_shots_group=self.player_shots,
                                                all_sprites_group=self.all_sprites))
                if tile == 2:
                    pos_x = column_counter * self.tile_size
                    pos_y = row_counter * self.tile_size

                    self.tile_list.append(Coin(coin_texture=coin_texture,
                                               position=(pos_x, pos_y),
                                               player_collision_group=self.player_collision_group,
                                               all_sprites_group=self.all_sprites))
                column_counter += 1
            row_counter += 1

    def stop(self):  # called when the state closes down
        self.should_transition = False

        if self.player is not None:
            self.player.kill()
            self.save_player_score()

        if self.all_sprites is not None:  # clear sprite group
            self.all_sprites.empty()
            self.all_sprites = None

        if self.player_shots is not None:  # clear sprite group
            self.player_shots.empty()
            self.player_shots = None

        if self.player_collision_group is not None:  # clear sprite group
            self.player_collision_group.empty()
            self.player_collision_group = None

        self.camera = None  # kill camera
        self.tile_list = []  # clear tiles

    def save_player_score(self):  # save player score into file
        player_data = []  # holds all data read from file
        with open('player_data.csv', 'r') as csv_file:  # read file into list
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:  # line is a dictionary
                player_data.append(line)  # add line to player data

        # increment player coins by loading the data then changing it
        #   then save it back
        player_coins = int(player_data[self.level - 1]['coins'])
        player_coins += self.player.coins_collected
        player_data[self.level - 1]['coins'] = player_coins

        with open('player_data.csv', 'w') as csv_file:  # re-write the data
            fieldnames = player_data[0].keys()  # field names shouldn't get deleted
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()  # re add the field names

            for line in player_data:  # write data back into file
                csv_writer.writerow(line)

    def process_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)
        self.player.process_events(event)

        if event.type == pygame.KEYDOWN:  # if any keyboard key is pressed
            if event.key == pygame.K_p:  # return to menu
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('KEY P pressed in LEVEL1STATE')

    def update(self, time_delta: float):  # update the elements
        self.camera.update(time_delta, self.player.position)  # update camera

        for tile in self.tile_list:  # update level
            tile.update(time_delta, self.camera)

        self.player.update(time_delta, self.camera)  # update player
        self.ui_manager.update(time_delta)  # update ui elements

    def draw(self):  # draw elements on screen
        # checks to see if the background should stop moving
        background_view_pos = (self.background_position[0] - self.camera.viewport_rect.left,
                               self.background_position[1] - self.camera.viewport_rect.top)
        self.window_surface.blit(self.background_texture, background_view_pos)  # draws background image onto display

        for tile in self.tile_list:  # draw level
            tile.draw(self.window_surface)

        self.player.draw(self.window_surface)  # draw player
        self.ui_manager.draw_ui(self.window_surface)





'''

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

from asteroid import Asteroid
from random import randint


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
        
        self.world_bounds = self.window_size
        
        # asteroid variables
        self.make_asteroid = False  # make an asteroid or not
        self.asteroid_texture = pygame.image.load('textures/asteroid.png').convert_alpha()
        self.asteroid_list = []  # contains all asteroids
        self.asteroid_creation_rate = 1.0  # time between asteroid creation
        self.asteroid_creation_timer = 0.0  # counter since last asteroid creation


        # level information
        self.level_data = [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def start(self):  # called when this state first appears
        
        world_centre = pygame.Vector2(self.window_size)
        self.camera = Camera(world_centre, pygame.Rect((0, 0), self.display_size),
                             pygame.Rect((0, 0), self.world_bounds))
        
        # add a background to the window
        self.background_surface = pygame.Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state
        
        # create sprite groups
        self.all_sprites = pygame.sprite.Group()

        # create player
        player_position = (self.window_surface.get_rect().centerx,
                           self.window_surface.get_rect().bottom - 50)
        player_image = pygame.image.load('level_states/game_images/gunman_2.png')
        player_bullet_image = pygame.image.load('level_states/game_images/laser2.png')
        
        self.player = Player(image=player_image,
                             bullet_image=player_bullet_image,
                             position=player_position,
                             all_sprites_group=self.all_sprites,
                             window_surface=self.window_surface)

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
        #self.player.update(time_delta, self.camera)
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
        '''
