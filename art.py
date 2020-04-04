"""
The artist's job is be as creative as possible in designing/coloring panels that their team occupies
Power skill: You are the face of your team - you are not only responsible for the final output that all other teams can see on the game board but also responsible for packaging and communicating it to the gameboard.
The team depends on your interfacing to score points and win the battle!
"""
import random
import time
import requests 
import socket
from socket_connector import PanelConnector

######################################

class ArtistDarkblue():
    """ The ArtistDarkblue class sends the artistic data to represent all players of the Game of Nanothrones.
    It includes custom animations to represent the Darkblue players in a novel way. 
    Relevant methods include:
    - send_data_to_panels(self, list_of_bytes)
    - communicate_with_style(self, game_state, panel_id_list)
    """

    def __init__(self,label, simulator = True):
        ### Do not edit the lines in this block of code
        ### These settings are essential for the game manager to connect 
        ### to the panel simulator
        self.label = label
        
    def send_data_to_panels(self, list_of_bytes):
        """Send data to the Nanoleaf simulator or to the Nanoleaf panels.
        list_of_bytes should contain a list of integers, each one between 0
        and 255."""
        PanelConnector().send_data_to_panels(list_of_bytes) 


    def regular_loop(self, game_state):
        """Takes self, game_state and creates list of bytes with Regular (accurate) Colors
        """
        rgb_list = {'brown': [131,81,32], 'red': [255,0,0], 'darkblue': [0,0,153], 'green': [25,250,70], 'lavender': [180,123,182], 'white':[255,255,255], 'crimson':[220,20,60], 'yellow':[255,255,0], 'purple': [127,0,255], 'orange':[255,127,80], 'pink': [255,20,147], 'black':[0,0,0], 'skyblue':[80,195,255] }
        rgb_blue_lighter = {'darkblue': [0,0,204]} 
        rgb_blue_lightest = {'darkblue': [0,0,255]}
        
        list_of_bytes = [0]
        panel_counter = 0

        for item in game_state['panel']: # REGULAR LOOP: Header loops through Panel ID keys: 1, 2, 3 and sends "regular" colors
            
            if game_state['panel'][item]['color'] != 'darkblue': # Non-darkblue tiles
                panel_counter += 1
                panel_num = item
                color = game_state['panel'][item].get('color')
                list_of_bytes.append(panel_num)
                list_of_bytes.append(1)
                list_of_bytes.append(rgb_list[color][0])
                list_of_bytes.append(rgb_list[color][1])
                list_of_bytes.append(rgb_list[color][2]) 
                list_of_bytes.append(0)
                list_of_bytes.append(1) 
            elif game_state['panel'][item]['color'] == 'darkblue' and game_state['panel'][item]['age'] < 2: # Darkblue tiles, Age < 2
                panel_counter += 1
                panel_num = item
                color = game_state['panel'][item].get('color')
                list_of_bytes.append(panel_num)
                list_of_bytes.append(1)
                list_of_bytes.append(rgb_list[color][0])
                list_of_bytes.append(rgb_list[color][1])
                list_of_bytes.append(rgb_list[color][2]) 
                list_of_bytes.append(0)
                list_of_bytes.append(1) 
            elif game_state['panel'][item]['color'] == 'darkblue' and game_state['panel'][item]['age'] == 2: # Darkblue tiles, Age 2
                panel_counter += 1
                panel_num = item
                color = game_state['panel'][item].get('color')
                list_of_bytes.append(panel_num)
                list_of_bytes.append(1)
                list_of_bytes.append(rgb_blue_lighter[color][0])
                list_of_bytes.append(rgb_blue_lighter[color][1])
                list_of_bytes.append(rgb_blue_lighter[color][2]) 
                list_of_bytes.append(0)
                list_of_bytes.append(1) 
            elif game_state['panel'][item]['color'] == 'darkblue' and game_state['panel'][item]['age'] > 2: # Darkblue tiles, Age > 2
                panel_counter += 1
                panel_num = item
                color = game_state['panel'][item].get('color')
                list_of_bytes.append(panel_num)
                list_of_bytes.append(1)
                list_of_bytes.append(rgb_blue_lightest[color][0])
                list_of_bytes.append(rgb_blue_lightest[color][1])
                list_of_bytes.append(rgb_blue_lightest[color][2]) 
                list_of_bytes.append(0)
                list_of_bytes.append(1) 
        list_of_bytes[0] = panel_counter 

        print(list_of_bytes)
        return(list_of_bytes)


    def party_loop(self, game_state):
        """Takes self, game_state and creates list of bytes with Party (random) Colors
        """
        rgb_list = {'brown': [131,81,32], 'red': [255,0,0], 'darkblue': [0,0,153], 'green': [25,250,70], 'lavender': [180,123,182], 'white':[255,255,255], 'crimson':[220,20,60], 'yellow':[255,255,0], 'purple': [127,0,255], 'orange':[255,127,80], 'pink': [255,20,147], 'black':[0,0,0], 'skyblue':[80,195,255] }
        rgb_party_time = {'magenta': [255,0,255], 'turquoise': [64,224,208], 'golden':[255,223,0]}
        
        list_of_bytes = [0]
        panel_counter = 0

        for item in game_state['panel']: # PARTY LOOP: Header loops through Panel ID keys: 1, 2, 3 and sends "party" colors (selects random party color)

             if game_state['panel'][item]['color'] != 'darkblue': # Non-darkblue tiles
                 panel_counter += 1
                 panel_num = item
                 color = game_state['panel'][item].get('color')
                 list_of_bytes.append(panel_num)
                 list_of_bytes.append(1)
                 list_of_bytes.append(rgb_list[color][0])
                 list_of_bytes.append(rgb_list[color][1])
                 list_of_bytes.append(rgb_list[color][2]) 
                 list_of_bytes.append(0)
                 list_of_bytes.append(1) 
             else: # Darkblue tiles, party color 
                 panel_counter += 1
                 panel_num = item
                 list_of_bytes.append(panel_num)
                 list_of_bytes.append(1)
                 list_of_bytes.extend(rgb_party_time[random.choice(list(rgb_party_time))])
                 list_of_bytes.append(0)
                 list_of_bytes.append(1) 
        list_of_bytes[0] = panel_counter 

        print(list_of_bytes)
        return(list_of_bytes)

    def communicate_with_style(self, game_state, panel_id_list):
        """ This function takes game_state (dictionary containing 'current state' and 'panel keys') as an input. 
        
        The game_state reflects the current state of Nanoleaf game. This function converts the game_state info into
        a list of bytes by calling two helper functions: regular_loop and party_loop. 

        It sends the list_of_bytes to pannels via helper function send_data_to_panels in order to update the colors. 
        the panel.

        For the darkblue tiles: 

          If the age <2, meaning the tile is blocked, the tile will be dark blue. 
          If the age == 2, meaning tile has just been unblocked, the tile becomes lighter blue.
          If age > 2, meaning the tile is unblocked but still alive (!) the tile becomes even lightest blue.

          All blue tiles will flash a random 'party color' before turning their desired shade. :)

        The function returns a print statement.
        """

        # Round 1 Byte Generator - Regular Colors
        self.send_data_to_panels(self.regular_loop(game_state)) # Sends list_of_bytes to panels via helper function (Round 1)
        time.sleep(.3)

        # Round 2 Byte Generator - ~*~* Party Round ~*~*
        self.send_data_to_panels(self.party_loop(game_state)) # Sends list_of_bytes to panels via helper function (Round 2)
        time.sleep(.3)

        # Round 3 Byte Generator - Regular Colors
        self.send_data_to_panels(self.regular_loop(game_state)) # Sends list_of_bytes to panels via helper function (Round 3)

        return(print('Artist in action :)'))