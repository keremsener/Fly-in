# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  map_generator.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/10 13:02:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 20:48:00 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import os
import random
from argparse import Namespace
from typing import Any, cast

from manim import (
    BLUE,
    GREEN,
    RED,
    WHITE,
    YELLOW,
    Circle,
    ImageMobject,
    Line,
    MovingCameraScene,
    Mobject,
    Square,
    Text,
    VGroup,
    tempconfig,
)
from manim.camera.moving_camera import MovingCamera

from src.core.error import ParsingError
from src.core.models import EndModel, HubModel, StartModel
from src.parsing.parsing import (
    parsing_connection,
    parsing_drone_func,
    parsing_hub_func,
)
from src.parsing.parsing_map_file import parsing_map_file
from .pathfinding import find_shortest_paths


class MovingAround(MovingCameraScene):
    """Manim scene rendering the hub network and animated drone flights."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize camera framing, optional background, and object maps."""
        super().__init__(**kwargs)
        camera = cast(MovingCamera, self.camera)
        camera.frame.move_to((5.0, 5.0, 0.0))
        camera.frame.set(width=22)

        self.bg_image: ImageMobject | None = None
        if os.path.exists("space.jpg"):
            self.bg_image = ImageMobject("space.jpg")
            self.bg_image.set_z_index(-10)
            self.add(self.bg_image)

        self.hub_mobjects: dict[str, Circle] = {}
        self.drone_mobjects: dict[str, VGroup] = {}

    def draw_hub(self, name: str, x: int, y: int, col: str) -> None:
        """Draw a circular node with label for a network hub."""
        try:
            circle = Circle(
                color=col,
                fill_opacity=1,
                arc_center=[x, y, 0],
                radius=0.5,
            )
        except Exception:
            circle = Circle(
                color="gray",
                fill_opacity=1,
                arc_center=[x, y, 0],
                radius=0.5,
            )
        label = Text(str(name), font_size=20).move_to(
            (float(x), float(y), 0.0)
        )
        self.add(circle, label)
        self.hub_mobjects[name] = circle

    def draw_conn(self, hub1_name: str, hub2_name: str) -> None:
        """Draw a connecting line between two existing hub mobjects."""
        start_circle = self.hub_mobjects.get(hub1_name)
        end_circle = self.hub_mobjects.get(hub2_name)

        if start_circle and end_circle:
            line = Line(
                start=start_circle.get_center(),
                end=end_circle.get_center(),
                color=YELLOW,
                buff=0.5,
            )
            line.set_z_index(-1)
            self.add(line)

    def play_turn(self, turn_str: str, start_hub_name: str) -> None:
        """Animate all drone transitions occurring within a single turn."""
        animations = []
        start_pos = self.hub_mobjects[start_hub_name].get_center()

        for move in turn_str.split():
            drone_id, target_spec = move.split("-", 1)
            if "-" in target_spec:
                orig_name, dest_name = target_spec.split("-", 1)
                orig_hub = self.hub_mobjects.get(orig_name)
                dest_hub = self.hub_mobjects.get(dest_name)
                if orig_hub and dest_hub:
                    target_pos = (
                        orig_hub.get_center() + dest_hub.get_center()
                    ) / 2
                else:
                    continue
            else:
                target_hub = self.hub_mobjects.get(target_spec)
                if not target_hub:
                    continue
                target_pos = target_hub.get_center()

            if drone_id not in self.drone_mobjects:
                square = Square(
                    side_length=0.35,
                    color=random.choice([RED, BLUE, GREEN, YELLOW]),
                    fill_opacity=1,
                )
                label = Text(drone_id, font_size=14, color=WHITE)
                drone = VGroup(square, label).move_to(start_pos)
                drone.set_z_index(2)
                self.add(drone)
                self.drone_mobjects[drone_id] = drone

            drone = self.drone_mobjects[drone_id]
            animations.append(drone.animate.move_to(target_pos))

        if animations:
            self.play(*animations, run_time=0.8)


def map_generate(
    hubs: list[Any],
    connections: list[tuple[str, str, int]],
    turn_logs: list[str],
    quality: str,
    preview: bool,
) -> None:
    """Configure Manim rendering options and execute the scene animation."""
    with tempconfig(
        {
            "quality": quality,
            "preview": preview,
            "disable_caching": True,
        }
    ):
        scene = MovingAround()
        camera = cast(MovingCamera, scene.camera)
        frame: Mobject = camera.frame
        start_hub: StartModel = hubs[0]
        end_hub: EndModel = hubs[1]
        middle_hubs: list[HubModel] = hubs[2]

        scene.draw_hub(
            start_hub.name, start_hub.x, start_hub.y, start_hub.color
        )
        scene.draw_hub(end_hub.name, end_hub.x, end_hub.y, end_hub.color)
        for hub in middle_hubs:
            scene.draw_hub(hub.name, hub.x, hub.y, hub.color)

        all_hubs = [start_hub, end_hub, *middle_hubs]
        xs = [h.x for h in all_hubs]
        ys = [h.y for h in all_hubs]
        frame.move_to(
            (
                (min(xs) + max(xs)) / 2,
                (min(ys) + max(ys)) / 2,
                0.0,
            )
        )
        frame.set(
            width=max(
                12.0,
                float(max(xs) - min(xs) + 4),
                float(max(ys) - min(ys) + 4) * 1.8,
            )
        )
        if scene.bg_image is not None:
            scene.bg_image.width = frame.width
            scene.bg_image.height = frame.height
            scene.bg_image.move_to(frame.get_center())

        for origin, dest, _ in connections:
            scene.draw_conn(origin, dest)
        for turn in turn_logs:
            scene.play_turn(turn, start_hub.name)

        scene.render()


def _print_turn_logs(turn_logs: list[str]) -> None:
    """Output simulation turn logs to stdout in subject format."""
    for turn in turn_logs:
        print(turn)


def map_generator() -> None:
    """Entry point orchestrating parsing, pathfinding, and visualization."""
    try:
        args: Namespace = parsing_map_file()
        map_path: str = args.map

        hubs = parsing_hub_func(map_path)
        drones = parsing_drone_func(map_path)
        all_connections = parsing_connection(map_path)
        state = find_shortest_paths(hubs, all_connections, drones)

        turn_logs: list[str] = state["turn_logs"]
        _print_turn_logs(turn_logs)

        if args.animate:
            map_generate(
                hubs,
                all_connections,
                turn_logs,
                quality=args.quality,
                preview=args.preview,
            )
    except (ParsingError, ValueError, RuntimeError) as error:
        print(f"Error: {error}")
