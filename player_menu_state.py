# import all libraries
# import pygame
from pygame import Surface, Rect
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton

# import parent class
from IAppState import IAppState


class PlayerMenuState(IAppState):

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.new_character_button = None
        self.equipment_button = None
        self.load_prior_data_button = None
        self.return_to_main_menu_button = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # create new character button
        new_character_button_pos_rect = Rect(0, 0, 150, 40)
        new_character_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        new_character_button_pos_rect.top = self.window_surface.get_height() * 0.4
        self.new_character_button = UIButton(relative_rect=new_character_button_pos_rect,
                                             text="New Character",
                                             manager=self.ui_manager)

        # create equipment button
        equipment_button_pos_rect = Rect(0, 0, 150, 40)
        equipment_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        equipment_button_pos_rect.top = new_character_button_pos_rect.bottom + 20
        self.equipment_button = UIButton(relative_rect=equipment_button_pos_rect,
                                                   text="Equipment",
                                                   manager=self.ui_manager)

        # create load prior data button
        load_prior_data_button_pos_rect = Rect(0, 0, 150, 40)
        load_prior_data_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        load_prior_data_button_pos_rect.top = equipment_button_pos_rect.bottom + 20
        self.load_prior_data_button = UIButton(relative_rect=load_prior_data_button_pos_rect,
                                                   text="Load Prior Data",
                                                   manager=self.ui_manager)

        # create return to main menu button
        return_to_main_menu_button_pos_rect = Rect(0, 0, 150, 40)
        return_to_main_menu_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        return_to_main_menu_button_pos_rect.top = load_prior_data_button_pos_rect.bottom + 20
        self.return_to_main_menu_button = UIButton(relative_rect=return_to_main_menu_button_pos_rect,
                                                   text="Return to main menu",
                                                   manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.return_to_main_menu_button.kill()  # destroy button
        self.return_to_main_menu_button = None  # reset button variable
        self.new_character_button.kill()
        self.new_character_button = None
        self.equipment_button.kill()
        self.equipment_button = None
        self.load_prior_data_button.kill()
        self.load_prior_data_button = None

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a button is pressed
            if event.ui_element == self.new_character_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'new_character_state'  # switch state
                print('NEW CHARACTER STATE button pressed in PLAYERMENUSTATE')

            if event.ui_element == self.equipment_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'equipment_state'  # switch state
                print('EQUIPMENT STATE button pressed in PLAYERMENUSTATE')

            if event.ui_element == self.load_prior_data_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'load_prior_data_state'  # switch state
                print('LOAD PRIOR 400DATA STATE button pressed in PLAYERMENUSTATE')

            if event.ui_element == self.return_to_main_menu_button:  # if return to main menu pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('RETURN MAIN MENU button pressed in PLAYERMENUSTATE')
