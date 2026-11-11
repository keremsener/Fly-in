# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_generator.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/10 13:02:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/11 11:37:56 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import parsing_hub_func, parsing_connection, parsing_start_end
from src.parsing.parsing_hub import HubParser
from src.error import ParsingError

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
        hubs = parsing_hub_func("map.txt")
        all_connections = parsing_connection("map.txt")
        start_hub = hubs.pop(0)
        end_hub = hubs.pop(0)
        print(hubs)
        print(end_hub)
    except ParsingError as error:
        print(f"Parsing error: {error}")