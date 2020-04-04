import json
from socket_connector import PanelConnector
import art
import strategy
import random
from random import sample

#########################

layout = PanelConnector().get_panel_layout().json()

######################################

### Creating instances
player_red = strategy.StrategistDarkblue(layout, 'red')
player_darkblue = strategy.StrategistDarkblue(layout, 'darkblue')
player_green = strategy.StrategistDarkblue(layout, 'green')
player_purple = strategy.StrategistDarkblue(layout, 'purple')
player_black = strategy.StrategistDarkblue(layout, 'black')
player_yellow = strategy.StrategistDarkblue(layout, 'yellow')

### Player_dict
player_dict = {'red' : player_red, 'darkblue' : player_darkblue, 'green' : player_green, 'purple' : player_purple, 'black' : player_black, 'yellow' : player_yellow}


### Basic settings
player_on_the_board = []
player_not_on_the_board = []
player_not_on_the_board = sample(list(player_dict.keys()), len(list(player_dict.keys())))
print(player_not_on_the_board)


### Creating game state
game_state = {}
game_state['current_position'] = {}
game_state['panel'] = {}
for key in list(player_dict.keys()):
    game_state['current_position'][key] = None
for item in range(len(layout['layout']['positionData'])):
    game_state['panel'][layout['layout']['positionData'][item]['panelId']] = {'color': 'white', 'age': 3}


### Functions
available_tiles = []    
def update_available_tiles():
    """When the loop wants to spawn a new player, it checks which tiles are available.
    """
    global available_tiles
    available_tiles = []
    for item in game_state['panel']:
        if game_state['panel'][item]['age'] >= 3:
            available_tiles.append(item)
        else:
            if item in available_tiles:
                available_tiles.remove(item)
            else:
                pass
    print("Available tiles :", available_tiles)
    
def update_age_for_the_color(color):
    """When a player moves, it updates other tiles age by 1.
    """
    for item in game_state['panel']:
        if game_state['panel'][item]['color'] == color:
            game_state['panel'][item]['age'] += 1
            print("    - Player {} in {} ages to {}".format(game_state['panel'][item]['color'], item, (game_state['panel'][item]['age'])))
     
def spawning():
    """Spawning players from player_not_on_the_board list.
    """
    global player_on_the_board
    global player_not_on_the_board
    update_available_tiles()
    player_on_the_board.append(player_not_on_the_board[0])
    game_state['current_position'][player_not_on_the_board[0]] = random.choice(available_tiles)
    game_state['panel'][game_state['current_position'][player_not_on_the_board[0]]]['color'] = player_not_on_the_board[0]
    game_state['panel'][game_state['current_position'][player_not_on_the_board[0]]]['age'] = 0
    del player_not_on_the_board[0]
        
          
turn_num = 0
def moving(item):
    """Moving players if the strategy returns a panelId.
    If it returns None, the player gets None value for their current_position,
    which will get them officially ejected by ejecting functions.
    """
    n_item = player_dict[item].next_move(game_state)
    print("    Player {} wants to move to".format(item), n_item)
    if n_item!= None:
        update_age_for_the_color(item)
        game_state['current_position'][item] = n_item
        game_state['panel'][game_state['current_position'][item]]['color'] = item
        game_state['panel'][game_state['current_position'][item]]['age'] = 0
        print("    Player {} successfully moved to".format(item), n_item)
        global turn_num
        turn_num += 1
    else:
        game_state['current_position'][item] = None
        print("    Player {} DIED".format(item))
     
def ejecting(item):
    """Ejecing the player by remove it from player_on_the_board and add it to player_not_on_the_board.
    """
    if game_state['current_position'][item] == None:
        player_on_the_board.remove(item)
        player_not_on_the_board.append(item)
        for i in game_state['panel']:
            if game_state['panel'][i]['color'] == item:
                game_state['panel'][i]['age'] = 3
                print("A {} color tile #{} unblocked".format(game_state['panel'][i]['color'], i))    

score = {}
for color in list(player_dict.keys()):
    score[color] = 0 
def keeping_score():    
    """Keeping score of each player. It is called at the end of every turn.
    """
    global score
    for item in game_state['panel']:
        for color in list(player_dict.keys()):
            if game_state['panel'][item]['color'] == color:
                score[color] += 1
    print("Score for the round :", score)
    
    
current_player_on_the_board = []    
same_players_turn = 1
spawn_max = 3
def spawn_max_increase():
    """To check if the board has been running for more than 50 turns without new spawning.
    If that's the case it increases spawn_max by 1. (Originally set at 3).
    """
    global current_player_on_the_board
    if player_on_the_board != current_player_on_the_board:
        current_player_on_the_board = player_on_the_board.copy()
        global same_players_turn
        same_players_turn = 1
    else: 
        same_players_turn += 1
    print("With {} list, it had {} turns at {}th iteration.".format(current_player_on_the_board, same_players_turn, n))
    if same_players_turn == 50:
        global spawn_max
        spawn_max += 1
        same_players_turn = 1
    
    

### Loops     
n = 1                
while n < 200:
    while len(player_on_the_board) < 3:
        spawning()
    spawn_max_increase()
    item = player_on_the_board[turn_num % len(player_on_the_board)]
    moving(item)
    ejecting(item)
    print("After {} iteration, ".format(n))
    keeping_score()
    print(game_state)
    art.ArtistDarkblue("darkblue").communicate_with_style(game_state, list(game_state['panel'].keys()))
    n += 1   