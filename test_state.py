# import all libraries
import pygame

from IAppState import IAppState

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton


class TestState(IAppState):

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: pygame.Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.test_button = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = pygame.Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # create test button button
        test_button_pos_rect = pygame.Rect(0, 0, 150, 40)
        test_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        test_button_pos_rect.top = self.window_surface.get_height() * 0.7
        self.test_button = UIButton(relative_rect=test_button_pos_rect,
                                    text="TEST RETURN MENU",
                                    manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.test_button.kill()  # destroy button
        self.test_button = None  # reset button variable

    def process_event(self, event: pygame.event.Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a button is pressed
            if event.ui_element == self.test_button:  # if test state button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to test state
                print('TEST STATE RETURN button pressed')
