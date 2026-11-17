# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_generator.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/10 13:02:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/17 13:13:07 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import parsing_hub_func, parsing_connection, parsing_drone_func
from src.core.error import ParsingError
from .pathfinding import find_shortest_paths
from src.parsing.parsing_map_file import parsing_map_file
from manim import *

class MovingAround(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.frame.move_to([5, 5, 0])
        self.camera.frame.set(width=22)
        self.hub_mobjects = {}

    def draw_hub(self, name, x, y, col):
        circle = Circle(
            color=col,
            fill_opacity=1,
            arc_center=[x, y, 0],
            radius=0.5
        )
        label = Text(str(name), font_size=20).move_to([x, y, 0])
        self.add(circle, label)
        self.hub_mobjects[name] = circle

    def draw_conn(self, hub1_name, hub2_name):
        start_circle = self.hub_mobjects.get(hub1_name)
        end_circle = self.hub_mobjects.get(hub2_name)

        if start_circle and end_circle:
            line = Line(
                start=start_circle.get_center(),
                end=end_circle.get_center(),
                color=YELLOW,
                buff=0.5
            )
            line.set_z_index(-1) 
            self.add(line)


def map_generate(hubs: list, connections: list):
    with tempconfig({
            "quality": "high_quality",
            "preview": True,
            "disable_caching": True
        }):
        scene = MovingAround()
        start_hub = hubs.pop(0)
        end_hub = hubs.pop(0)
        scene.draw_hub(start_hub.name, start_hub.x, start_hub.y, start_hub.color)
        scene.draw_hub(end_hub.name, end_hub.x, end_hub.y, end_hub.color)
        [scene.draw_hub(hub.name, hub.x, hub.y, hub.color) for hub in hubs[0]]
        [scene.draw_conn(conn[0], conn[1]) for conn in connections]

        scene.render()



def map_generator():
    try:
        hubs = parsing_hub_func(parsing_map_file())
        drones = parsing_drone_func(parsing_map_file())
        all_connections = parsing_connection(parsing_map_file())
        state = find_shortest_paths(hubs, all_connections, drones)
        for line in state["turn_logs"]:
            print(line)

        map_generate(hubs, all_connections) 
    except (ParsingError, ValueError, RuntimeError) as error:
        print(f"Error: {error}")
