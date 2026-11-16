# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_generator.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/10 13:02:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/16 14:33:39 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import parsing_hub_func, parsing_connection, parsing_drone_func, parsing_start_end
from src.parsing.parsing_hub import HubParser
from src.error import ParsingError
from .pathfinding import find_shortest_paths
from src.parsing.parsing_map_file import parsing_map_file
# ------------------- TASK ----------------------------
# def map_border_maker(start_x: int, start_y: int, goal_x: int, goal_y: int):
    # x = 0
    # y = 0
    # init_x = start_x
    # map_coordinates = []
    # for start_y in range(goal_y + 2):
        # for start_x in range(goal_x + 1):
            # print(".", end="")
            # x = start_x
            # map_coordinates.append((x, y))

        # print()
        # y = start_y
        # start_x = init_x
    # print(map_coordinates)



def map_generator():
    try:
        hubs = parsing_hub_func(parsing_map_file())
        drones = parsing_drone_func(parsing_map_file())
        all_connections = parsing_connection(parsing_map_file())
        state = find_shortest_paths(hubs, all_connections, drones)
        for line in state["turn_logs"]:
            print(line)
    except (ParsingError, ValueError, RuntimeError) as error:
        print(f"Error: {error}")