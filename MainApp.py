# import all libraries
import pygame

from pygame_gui import UIManager

from initial_state import InitialState
from main_menu_state import MainMenuState
from select_level_state import SelectLevelState
from test_state import TestState
from options_state import OptionsState
from high_scores_state import HighScoresState
from character_design_state import CharacterDesignState
from player_menu_state import PlayerMenuState
from new_character_state import NewCharacterState
from equipment_state import EquipmentState
from load_prior_data_state import LoadPriorDataState
from level_1_state import Level1State


# Create main game app
class MainApp:

    def __init__(self):

        pygame.init()  # initialise pygame

        self.window_size = (800, 600)  # create window size
        self.window_surface = pygame.display.set_mode(self.window_size)  # create a window

        self.ui_manager = UIManager(self.window_size)  # create ui manager

        # dictionary that holds all state classes
        self.all_states = {'initial_state': InitialState(self.window_surface,
                                                         self.window_size,
                                                         self.ui_manager),
                           'main_menu_state': MainMenuState(self.window_surface,
                                                            self.window_size,
                                                            self.ui_manager),
                           'select_level_state': SelectLevelState(self.window_surface,
                                                                  self.window_size,
                                                                  self.ui_manager),
                           'test_state': TestState(self.window_surface,
                                                   self.window_size,
                                                   self.ui_manager),
                           'options_state': OptionsState(self.window_surface,
                                                         self.window_size,
                                                         self.ui_manager),
                           'high_scores_state': HighScoresState(self.window_surface,
                                                                self.window_size,
                                                                self.ui_manager),
                           'character_design_state': CharacterDesignState(self.window_surface,
                                                                          self.window_size,
                                                                          self.ui_manager),
                           'player_menu_state': PlayerMenuState(self.window_surface,
                                                                self.window_size,
                                                                self.ui_manager),
                           'new_character_state': NewCharacterState(self.window_surface,
                                                                    self.window_size,
                                                                    self.ui_manager),
                           'equipment_state': EquipmentState(self.window_surface,
                                                             self.window_size,
                                                             self.ui_manager),
                           'load_prior_data_state': LoadPriorDataState(self.window_surface,
                                                                       self.window_size,
                                                                       self.ui_manager),
                           'level_1_state': Level1State(self.window_surface,
                                                        self.window_size,
                                                        self.ui_manager)
                           }

        # set active state to main menu initially
        self.active_state = self.all_states['initial_state']
        self.active_state.start()  # call start func of InitialState

        self.clock = pygame.time.Clock()  # create a clock
        self.is_running = True

    # main game loop
    def run(self):
        while self.is_running:  # check if running
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():  # receive events
                if event.type == pygame.QUIT:  # if X button is pressed
                    self.is_running = False  # quit game

                self.active_state.process_event(event)  # process all events
                self.check_state_should_transition()  # check states should transition

            self.active_state.update(time_delta)  # update called every while loop

            self.active_state.draw()  # call draw func

            pygame.display.flip()  # send all changes to window

    def check_state_should_transition(self):  # check if a state switch should happen
        if self.active_state.get_should_transition():  # Returns True/False
            if self.active_state.transition_target in self.all_states:  # check if target is not EXIT
                transition_target = self.active_state.get_transition_target()  # returns a string
                self.active_state.stop()  # destroy all elements in that state
                self.active_state = self.all_states[transition_target]  # get the new state from the dictionary
                self.active_state.start()  # start up the new state
            elif self.active_state.transition_target == 'exit_app':
                self.is_running = False


# create app and run it
main_app = MainApp()
main_app.run()
