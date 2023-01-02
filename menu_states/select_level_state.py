# import pygame
from pygame import Surface, Rect
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton

# import parent class
from IAppState import IAppState


class SelectLevelState(IAppState):  # class inherits from IAppState

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.level_1_button = None
        self.level_2_button = None
        self.level_3_button = None
        self.level_4_button = None
        self.return_to_main_menu_button = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # create level 1 button
        level_1_button_pos_rect = Rect(0, 0, 150, 40)
        level_1_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        level_1_button_pos_rect.top = self.window_surface.get_height() * 0.4
        self.level_1_button = UIButton(relative_rect=level_1_button_pos_rect,
                                       text="Level 1",
                                       manager=self.ui_manager)

        # create level 2 button
        level_2_button_pos_rect = Rect(0, 0, 150, 40)
        level_2_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        level_2_button_pos_rect.top = level_1_button_pos_rect.bottom + 20
        self.level_2_button = UIButton(relative_rect=level_2_button_pos_rect,
                                       text="Level 2",
                                       manager=self.ui_manager)

        # create level 2 button
        level_3_button_pos_rect = Rect(0, 0, 150, 40)
        level_3_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        level_3_button_pos_rect.top = level_2_button_pos_rect.bottom + 20
        self.level_3_button = UIButton(relative_rect=level_3_button_pos_rect,
                                       text="Level 3",
                                       manager=self.ui_manager)

        # create level 2 button
        level_4_button_pos_rect = Rect(0, 0, 150, 40)
        level_4_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        level_4_button_pos_rect.top = level_3_button_pos_rect.bottom + 20
        self.level_4_button = UIButton(relative_rect=level_4_button_pos_rect,
                                       text="Level 4",
                                       manager=self.ui_manager)

        # create return to main menu button
        return_to_main_menu_button_pos_rect = Rect(0, 0, 150, 40)
        return_to_main_menu_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        return_to_main_menu_button_pos_rect.top = level_4_button_pos_rect.bottom + 20
        self.return_to_main_menu_button = UIButton(relative_rect=return_to_main_menu_button_pos_rect,
                                                   text="Return to main menu",
                                                   manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.level_1_button.kill()
        self.level_1_button = None
        self.level_2_button.kill()
        self.level_2_button = None
        self.level_3_button.kill()
        self.level_3_button = None
        self.level_4_button.kill()
        self.level_4_button = None
        self.return_to_main_menu_button.kill()  # destroy button
        self.return_to_main_menu_button = None  # reset button variable

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a button is pressed

            if event.ui_element == self.level_1_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'level_1_state'  # switch state
                print('LEVEL 1 button pressed in SELECTLEVELSTATE')

            if event.ui_element == self.level_2_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'level_2_state'  # switch state
                print('LEVEL 2 button pressed in SELECTLEVELSTATE')

            if event.ui_element == self.level_3_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'level_3_state'  # switch state
                print('LEVEL 3 button pressed in SELECTLEVELSTATE')

            if event.ui_element == self.level_4_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'level_4_state'  # switch state
                print('LEVEL 4 button pressed in SELECTLEVELSTATE')

            if event.ui_element == self.return_to_main_menu_button:  # if return to main menu pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('RETURN MAIN MENU button pressed in SELECTLEVELSTATE')
