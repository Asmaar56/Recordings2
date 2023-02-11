# import pygame
from pygame import Surface, Rect
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel

# import parent class
from IAppState import IAppState


class DefeatState(IAppState):  # class inherits from IAppState

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.return_to_player_menu_button = None
        self.defeat_label = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        defeat_text_label_pos_rect = Rect(0, 0, 400, 40)
        defeat_text_label_pos_rect.centerx = self.window_surface.get_rect().centerx
        defeat_text_label_pos_rect.top = self.window_surface.get_height() * 0.3
        self.defeat_label = UILabel(relative_rect=defeat_text_label_pos_rect,
                                    text="Game over",
                                    manager=self.ui_manager)

        # create return to player menu button
        return_to_player_menu_button_pos_rect = Rect(0, 0, 150, 40)
        return_to_player_menu_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        return_to_player_menu_button_pos_rect.top = defeat_text_label_pos_rect.bottom + 20
        self.return_to_player_menu_button = UIButton(relative_rect=return_to_player_menu_button_pos_rect,
                                                     text="Return to main menu",
                                                     manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.return_to_player_menu_button.kill()  # destroy button
        self.return_to_player_menu_button = None  # reset button variable
        self.defeat_label.kill()
        self.defeat_label = None

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a button is pressed
            if event.ui_element == self.return_to_player_menu_button:  # if return to player menu pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to player menu
                print('RETURN MAIN MENU button pressed in DEFEATSTATE')
