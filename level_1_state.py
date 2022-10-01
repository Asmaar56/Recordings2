# import all libraries
import pygame

from IAppState import IAppState
from player import Player
from object_1 import Object1

from pygame_gui import UIManager
from pygame import KEYDOWN


class Level1State(IAppState):

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

        self.tile_list = []
        self.tile_size = 50
        self.block_img = pygame.image.load('game-images/block.png')

        self.worldData = [
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

        # create obstacles
        object_1_position = (self.window_surface.get_rect().centerx + 100,
                             self.window_surface.get_rect().bottom - 100)

        self.object_1 = Object1(object_1_position)
        self.make_world()


    def make_world(self):

        row_counter = 0
        for row in self.worldData:
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

        self.player = None

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

    def draw(self):  # draws buttons onto window
        self.window_surface.blit(self.background_surface, (0, 0))
        for tile in self.tile_list:
            self.window_surface.blit(tile[0], tile[1])

        self.ui_manager.draw_ui(self.window_surface)  # draws ui elements onto window
        self.player.draw(self.window_surface)
        self.object_1.draw(self.window_surface)
        # pygame.draw.rect(self.window_surface, self.player.colour, self.player.pos_rect)

