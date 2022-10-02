# import pygame
from pygame import Surface, Rect, KEYDOWN
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UILabel

# import parent class
from IAppState import IAppState


class InitialState(IAppState):

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,  # receive background_surface here
                         window_size,
                         ui_manager)

        # text box variables
        self.press_any_to_begin_text_label = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        press_any_to_begin_text_label_pos_rect = Rect(0, 0, 400, 40)
        press_any_to_begin_text_label_pos_rect.centerx = self.window_surface.get_rect().centerx
        press_any_to_begin_text_label_pos_rect.top = self.window_surface.get_rect().centery
        self.press_any_to_begin_text_label = UILabel(relative_rect=press_any_to_begin_text_label_pos_rect,
                                                     text="Press any button to begin",
                                                     manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.press_any_to_begin_text_label.kill()
        self.press_any_to_begin_text_label = None

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == KEYDOWN:  # if any keyboard key is pressed
            self.should_transition = True  # this is returned in return_should_transition()
            self.transition_target = 'main_menu_state'  # switch to main menu
            print('KEYBOARD pressed in INITIALSTATE')
