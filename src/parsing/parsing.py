# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:10:36 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from src.core.error import ParsingError, ValidationParsingError
from src.core.models import Drone, EndModel, HubModel, StartModel
from .parsing_conn import ConnParser
from .parsing_hub import parsing_hub


class MapParser:
    """High-level coordinator converting raw map files into Pydantic models."""

    def __init__(self, file_path: str) -> None:
        """Initialize parser with the path to a map file."""
        self.file_path: str = file_path
        self.start_model: StartModel | None = None
        self.end_model: EndModel | None = None
        self.nb_drones: int = 0

    def _to_models(self, hubs: list[dict[str, Any]]) -> list[HubModel]:
        """Convert raw hub dictionaries into validated HubModel instances."""
        hub_list: list[HubModel] = []
        for item in hubs:
            hub_model = HubModel(
                name=item["name"],
                x=int(item["x"]),
                y=int(item["y"]),
                neighbor=item.get("neighbor", {}),
                color=item.get("color", "gray"),
                zone=item.get("zone", "normal"),
                max_drones=int(item.get("max_drones", 1)),
            )
            hub_list.append(hub_model)
        return hub_list

    def _extract_nb_drones(self, lines: list[str]) -> int:
        """Validate and extract 'nb_drones' from the first non-comment line."""
        for line_num, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("nb_drones:"):
                raise ValidationParsingError(
                    f"Line {line_num}: First directive must be 'nb_drones:'."
                )
            try:
                nb_drones = int(line.split(":", 1)[1].strip())
            except ValueError as exc:
                raise ValidationParsingError(
                    f"Line {line_num}: 'nb_drones' must be an integer."
                ) from exc
            if nb_drones < 1:
                raise ValidationParsingError(
                    f"Line {line_num}: Drone count must be positive."
                )
            return nb_drones
        raise ValidationParsingError(
            "'nb_drones' field is missing in map file.")

    def parse(self) -> list[Any]:
        """Parse map file into [StartModel, EndModel, list[HubModel]]."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except OSError as exc:
            raise ValidationParsingError(
                f"Cannot open map file '{self.file_path}': {exc}"
            ) from exc

        try:
            self.nb_drones = self._extract_nb_drones(lines)
            start_hub, end_hub, hubs = parsing_hub(lines)

            self.start_model = StartModel(
                name=start_hub["name"],
                x=int(start_hub["x"]),
                y=int(start_hub["y"]),
                neighbor=start_hub.get("neighbor", {}),
                color=start_hub.get("color", "green"),
            )
            self.end_model = EndModel(
                name=end_hub["name"],
                x=int(end_hub["x"]),
                y=int(end_hub["y"]),
                neighbor=end_hub.get("neighbor", {}),
                color=end_hub.get("color", "yellow"),
            )
            return [self.start_model, self.end_model, self._to_models(hubs)]
        except ParsingError:
            raise
        except Exception as exc:
            raise ValidationParsingError(f"Map parsing failed: {exc}") from exc

    def parse_drones(self) -> list[Drone]:
        """Initialize the requested number of Drone objects at start_hub."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            self.nb_drones = self._extract_nb_drones(lines)
            start_hub, _, _ = parsing_hub(lines)

            if not start_hub.get("name"):
                raise ValidationParsingError(
                    "Start hub could not be parsed for drone initialization."
                )

            return [
                Drone(id=drone_id, current_location=start_hub["name"])
                for drone_id in range(1, self.nb_drones + 1)
            ]
        except ParsingError:
            raise
        except Exception as exc:
            raise ValidationParsingError(
                f"Drone parsing failed: {exc}"
            ) from exc


def validate_connection(
    parsed_list: list[tuple[str, str, int]], file_path: str
) -> bool:
    """Ensure connections reference valid hubs without duplicates."""
    seen_connections: set[tuple[str, str]] = set()
    with open(file_path, "r", encoding="utf-8") as file:
        start_hub, end_hub, hubs = parsing_hub(file)

    hub_name_set: set[str] = {start_hub["name"], end_hub["name"]}
    for hub in hubs:
        hub_name_set.add(hub["name"])

    for origin, dest, max_link_cap in parsed_list:
        if origin not in hub_name_set or dest not in hub_name_set:
            return False
        if origin == dest:
            return False
        if int(max_link_cap) < 1:
            return False

        pair = sorted([origin, dest])
        connection_pair = (pair[0], pair[1])
        if connection_pair in seen_connections:
            return False

        seen_connections.add(connection_pair)

    return True


def parsing_connection(file_path: str) -> list[tuple[str, str, int]]:
    """Parse and validate all connections from the given map file."""
    parsed_connection = ConnParser(file_path).parse_all()
    if validate_connection(parsed_connection, file_path):
        return parsed_connection
    raise ValidationParsingError(
        "Connection validation failed: unknown hub name or duplicate link."
    )


def parsing_hub_func(file_path: str) -> list[Any]:
    """Parse hubs from file path."""
    return MapParser(file_path).parse()


def parsing_drone_func(file_path: str) -> list[Drone]:
    """Parse drones from file path."""
    return MapParser(file_path).parse_drones()
