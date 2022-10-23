# import pygame
from pygame import Surface, Rect
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton

# import parent class
from IAppState import IAppState


class MainMenuState(IAppState):  # class inherits from IAppState

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.test_button = None
        self.select_level_button = None
        self.high_scores_button = None
        self.options_button = None
        self.character_design_button = None
        self.player_menu_button = None
        self.exit_button = None

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # create select_level button
        select_level_button_pos_rect = Rect(0, 0, 150, 40)
        select_level_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        select_level_button_pos_rect.top = self.window_surface.get_height() * 0.4
        self.select_level_button = UIButton(relative_rect=select_level_button_pos_rect,
                                            text="Select Level",
                                            manager=self.ui_manager)
        # create test button
        test_button_pos_rect = Rect(0, 0, 150, 40)
        test_button_pos_rect.centerx = 100
        test_button_pos_rect.top = 22
        self.test_button = UIButton(relative_rect=test_button_pos_rect,
                                    text="Test state",
                                    manager=self.ui_manager)

        # create options button
        options_button_pos_rect = Rect(0, 0, 150, 40)
        options_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        options_button_pos_rect.top = select_level_button_pos_rect.bottom + 20
        self.options_button = UIButton(relative_rect=options_button_pos_rect,
                                       text="Options",
                                       manager=self.ui_manager)

        # create high scores button
        high_scores_button_pos_rect = Rect(0, 0, 150, 40)
        high_scores_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        high_scores_button_pos_rect.top = options_button_pos_rect.bottom + 20
        self.high_scores_button = UIButton(relative_rect=high_scores_button_pos_rect,
                                           text="High Scores",
                                           manager=self.ui_manager)

        # create character design button
        character_design_button_pos_rect = Rect(0, 0, 150, 40)
        character_design_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        character_design_button_pos_rect.top = high_scores_button_pos_rect.bottom + 20
        self.character_design_button = UIButton(relative_rect=character_design_button_pos_rect,
                                                text="Character Design",
                                                manager=self.ui_manager)

        # create player menu button
        player_menu_button_pos_rect = Rect(0, 0, 150, 40)
        player_menu_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        player_menu_button_pos_rect.top = character_design_button_pos_rect.bottom + 20
        self.player_menu_button = UIButton(relative_rect=player_menu_button_pos_rect,
                                           text="Player Menu",
                                           manager=self.ui_manager)

        # create exit button
        exit_button_pos_rect = Rect(0, 0, 150, 40)
        exit_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        exit_button_pos_rect.top = player_menu_button_pos_rect.bottom + 20
        self.exit_button = UIButton(relative_rect=exit_button_pos_rect,
                                    text="Exit",
                                    manager=self.ui_manager)

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.select_level_button.kill()  # destroy button
        self.select_level_button = None  # reset button variable
        self.test_button.kill()
        self.test_button = None
        self.options_button.kill()
        self.options_button = None
        self.high_scores_button.kill()
        self.high_scores_button = None
        self.character_design_button.kill()
        self.character_design_button = None
        self.player_menu_button.kill()
        self.player_menu_button = None
        self.exit_button.kill()
        self.exit_button = None

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a UIBUTTON is pressed
            if event.ui_element == self.select_level_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'select_level_state'  # switch state
                print('SELECT LEVEL button pressed in MAINMENUSTATE')

            if event.ui_element == self.test_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'test_state'  # switch state
                print('TEST STATE button pressed in MAINMENUSTATE')

            if event.ui_element == self.options_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'options_state'  # switch state
                print('OPTIONS STATE button pressed in MAINMENUSTATE')

            if event.ui_element == self.high_scores_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'high_scores_state'  # switch state
                print('HIGH SCORES STATE button pressed in MAINMENUSTATE')

            if event.ui_element == self.character_design_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'character_design_state'  # switch state
                print('CHARACTER DESIGN STATE button pressed in MAINMENUSTATE')

            if event.ui_element == self.player_menu_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'player_menu_state'  # switch state
                print('PLAYER MENU STATE button pressed in MAINMENUSTATE')

            if event.ui_element == self.exit_button:  # if button pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'exit_app'  # switch state
                print('EXIT APP button pressed in MAINMENUSTATE')
