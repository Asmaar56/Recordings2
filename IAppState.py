import pygame

from pygame_gui import UIManager


class IAppState:

    def __init__(self,
                 window_surface: pygame.Surface,
                 window_size,
                 ui_manager: UIManager):

        # admin variables
        self.window_surface = window_surface
        self.window_size = window_size
        self.ui_manager = ui_manager

        # transition variables
        self.transition_target = 'None'
        self.should_transition = False

        # create background variable
        self.background_surface = None

    def start(self):
        # add a background to the window
        self.background_surface = pygame.Surface(self.window_size)
        self.background_surface.fill((0, 0, 0)) # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

    def get_should_transition(self):  # check if should transition or not
        return self.should_transition  # returns True/False

    def get_transition_target(self):  # gets transition target
        return self.transition_target

    def update(self, time_delta: float):  # update takes time as parameter
        self.ui_manager.update(time_delta=time_delta)

    def process_event(self, event: pygame.event.Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

    def draw(self):  # draws buttons onto window
        self.window_surface.blit(self.background_surface, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)  # draws ui elements onto window
