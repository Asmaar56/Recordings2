import csv

# import pygame
from pygame import Surface, Rect
from pygame.event import Event

# import pygame_gui
from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton, UILabel

# import parent class
from IAppState import IAppState


class HighScoresState(IAppState):  # class inherits from IAppState

    # init takes 2 parameters: window_surface and ui_manager from MainApp
    def __init__(self,
                 window_surface: Surface,
                 window_size,
                 ui_manager: UIManager):

        super().__init__(window_surface,
                         window_size,
                         ui_manager)

        # button variables
        self.return_to_main_menu_button = None

        self.level_labels_list = []

    def start(self):  # called when this state first appears

        # add a background to the window
        self.background_surface = Surface(self.window_size)
        self.background_surface.fill((0, 0, 0))  # set background to black so it erases all button images

        self.should_transition = False  # should switch to another state?
        self.transition_target = 'None'  # target state?

        # create return to main menu button
        return_to_main_menu_button_rect = Rect(0, 0, 150, 40)
        return_to_main_menu_button_rect.centerx = self.window_surface.get_rect().centerx
        return_to_main_menu_button_rect.top = self.window_surface.get_height() * 0.8
        self.return_to_main_menu_button = UIButton(relative_rect=return_to_main_menu_button_rect,
                                                   text="Return to main menu",
                                                   manager=self.ui_manager)
        self.load_high_scores()

    def load_high_scores(self):
        high_scores_data = []
        with open('player_data.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                high_scores_data.append(line)

        label_position_increment = 0
        for level_data in high_scores_data:

            # relative_rect
            label_pos_rect = Rect(0, 0, 400, 40)
            label_pos_rect.centerx = self.window_surface.get_rect().centerx
            label_pos_rect.top = (self.window_surface.get_height() * 0.2) + label_position_increment

            label_text = 'Level ' + level_data['level'] + \
                         ' | coins collected: ' + level_data['coins'] + \
                         '| kills: ' + level_data['kills']

            # make uiLabel
            self.level_labels_list.append(
                UILabel(relative_rect=label_pos_rect,
                        text=label_text,
                        manager=self.ui_manager)
            )
            label_position_increment += 100

    def stop(self):  # called when state is closed
        self.background_surface = None  # remove background

        self.return_to_main_menu_button.kill()  # destroy button
        self.return_to_main_menu_button = None  # reset button variable

        for label in self.level_labels_list:
            label.kill()
        self.level_labels_list = []

    def process_event(self, event: Event):  # takes event as parameter
        self.ui_manager.process_events(event)  # call  builtin process_events

        if event.type == UI_BUTTON_PRESSED:  # if a button is pressed
            if event.ui_element == self.return_to_main_menu_button:  # if return to main menu pressed
                self.should_transition = True  # this is returned in return_should_transition()
                self.transition_target = 'main_menu_state'  # switch to main menu
                print('RETURN MAIN MENU button pressed in HIGHSCORESTATE')
