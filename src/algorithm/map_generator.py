# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_generator.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/10 13:02:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/17 13:01:03 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import parsing_hub_func, parsing_connection, parsing_drone_func
from src.core.error import ParsingError
from .pathfinding import find_shortest_paths
from src.parsing.parsing_map_file import parsing_map_file
from manim import *

class MovingAround(MovingCameraScene):
    def draw_hub(self, x, y, col):
        self.camera.frame.move_to([5, 5, 0])
        self.camera.frame.set(width=22)
        circle = Circle(color=col, fill_opacity=1, arc_center=[x, y, 0], radius=0.5)
        self.add(circle)


def map_generate(hubs: list):
    with tempconfig({
            "quality": "high_quality",
            "preview": True,
            "disable_caching": True
        }):
        scene = MovingAround()
        start_hub = hubs.pop(0)
        end_hub = hubs.pop(0)
        scene.draw_hub(start_hub.x, start_hub.y, start_hub.color)
        scene.draw_hub(end_hub.x, end_hub.y, end_hub.color)
        [scene.draw_hub(hub.x, hub.y, hub.color) for hub in hubs[0]]
        scene.render()


def map_generator():
    try:
        hubs = parsing_hub_func(parsing_map_file())
        drones = parsing_drone_func(parsing_map_file())
        all_connections = parsing_connection(parsing_map_file())
        state = find_shortest_paths(hubs, all_connections, drones)
        for line in state["turn_logs"]:
            print(line)
        map_generate(hubs)
    except (ParsingError, ValueError, RuntimeError) as error:
        print(f"Error: {error}")