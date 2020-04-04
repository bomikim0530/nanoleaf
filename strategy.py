"""
Dark Blue will consider both defensive and offensive strategies to stay on the board as long as possible and block as many
competitors as possible.

"""
import random
import operator

class StrategistDarkblue():
    
    neighbor_dict = {} 
    def __init__(self, layout, label):
        """Set up dark blue player:
        Parameters:
        layout: Nanoleaf panel layout
        label: handle for player during game
        """
        self.neighbors = self.get_neighbors(layout)
        self.label = label 
    
    def get_neighbors(self, layout):
        """Find neighbors of every panel on board using x, y coordinates.
        Return neighbor dictionary wherein keys are IDs of each panel and values are IDs of all of their neighbors.
        """
        for elements in layout['layout']['positionData']:
            this_element = elements
            self.neighbor_dict[this_element['panelId']] = []
            for elements in layout['layout']['positionData']:
                if this_element['o'] == 0:
                    if elements['x'] == this_element['x'] + 75 or elements['x'] == this_element['x'] - 75:
                        if elements['y'] == this_element['y'] + 43:
                            self.neighbor_dict[this_element['panelId']].append(elements['panelId'])
                    elif elements['x'] == this_element['x']:
                        if elements['y'] == this_element['y'] - 87:
                            self.neighbor_dict[this_element['panelId']].append(elements['panelId'])
                elif this_element['o'] == 60:
                    if elements['x'] == this_element['x'] + 75 or elements['x'] == this_element['x'] - 75:
                        if elements['y'] == this_element['y'] - 43:
                            self.neighbor_dict[this_element['panelId']].append(elements['panelId'])
                    elif elements['x'] == this_element['x']:
                        if elements['y'] == this_element['y'] + 87:
                            self.neighbor_dict[this_element['panelId']].append(elements['panelId'])

    def next_move(self, game_state):
        """
        Create and select strategy to use for next move:
        Parameters:
        game_state: current environment of board providing panels, and their associated colors (which players they're occupied by),
        as well as associated ages
        - available_tiles: age 3 or greater (and thus open to move into)
        - other_players_are: age = 0 (and therefore players' current positions)
        - other_players_with_neighbors = other players' neighbors
        - neighbors_with_neighbors = neighbors' neighbors
        If no next moves, ejected from board with error message.
        If opponents' tiles available to block, block.
        Or move to own neighbors with the most neighbors. 
        """
        current_position_me = game_state['current_position'][self.label]
        available_tile = []
        lets_go = 0
        for item in self.neighbor_dict[current_position_me]:
            if game_state['panel'][item]['age'] >= 3:
                available_tile.append(item)
            else:
                pass
        if len(available_tile) == 0:
            return None
        else: 
            other_players_are = []
            for item in game_state['panel'].keys():
                if game_state['panel'][item]['age'] == 0:
                    other_players_are.append(item)
                else:
                    pass
            others_neighbor = []
            for item in other_players_are:
                others_neighbor.append(self.neighbor_dict[item])
            for item in available_tile:
                neighbor_num_dict = {}
                neighbor_num_dict[item] = self.neighbor_dict[item]
                if item in others_neighbor:
                    lets_go = item
                else:
                    lets_go = max(neighbor_num_dict.items(), key=operator.itemgetter(1))[0]
            return lets_go