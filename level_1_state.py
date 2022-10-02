# import libraries
import pygame

# import parent class
from IAppState import IAppState

# import elements and events
from pygame_gui import UIManager
from pygame import KEYDOWN

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
        self.player = None
        self.object_1 = None

        # level variables
        self.tile_list = []
        self.tile_size = 50
        self.block_img = pygame.image.load('game-images/block.png')

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

        # create player
        player_position = (self.window_surface.get_rect().centerx,
                           self.window_surface.get_rect().bottom - 50)
        self.player = Player(player_position)

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
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                column_counter += 1
            row_counter += 1

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.player = None  # kill player

    def process_event(self, event: pygame.event.Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == KEYDOWN:  # if any keyboard key is pressed
            if event.key == pygame.K_p: # return to menu
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('KEY P pressed in LEVEL1STATE')

    def update(self, time_delta: float):  # update takes time as parameter
        self.player.update(time_delta)
        self.object_1.update(time_delta)
        self.ui_manager.update(time_delta=time_delta)

    def draw(self):  # draw changes onto window
        self.window_surface.blit(self.background_surface, (0, 0))

        for tile in self.tile_list:  # draw level
            self.window_surface.blit(tile[0], tile[1])

        self.ui_manager.draw_ui(self.window_surface)  # draws ui elements onto window
        self.player.draw(self.window_surface)
        self.object_1.draw(self.window_surface)

