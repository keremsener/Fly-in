# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_hub.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:39:15 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 11:41:39 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from enum import Enum


class HubOptions(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class HubParser:
    def __init__(self):
        self.start_hub = {"name": "", "x": "", "y": "", "color": ""}
        self.end_hub = {"name": "", "x": "", "y": "", "color": ""}
        self.hubs = []

    def reset(self):
        self.start_hub = {"name": "", "x": "", "y": "", "color": ""}
        self.end_hub = {"name": "", "x": "", "y": "", "color": ""}
        self.hubs = []

    def _validate_coordinates(self, x_value: str, y_value: str, hub_name: str):
        if int(x_value) < 0 or int(y_value) < 0:
            raise Exception(
                f"Coordinates for '{hub_name}' must be positive values.")

    def _parse_hub_attributes(self, hub: dict, rest: list[str]):
        for i, item in enumerate(rest):
            if i == 0 and item.startswith("["):
                item = item[1:]
            if i == len(rest) - 1 and item.endswith("]"):
                item = item[:-1]

            if "=" in item:
                key, value = item.split("=", 1)
                valid_keys = {option.value for option in HubOptions}
                if key not in valid_keys:
                    raise Exception(
                        f"'{key}' is not match Hub options. "
                        f"Did you mean 'zone', 'color', 'max_drones'?")
                hub[key] = value

    def _parse_start_hub(self, line: str):
        parts = line.split()
        self.start_hub["name"] = parts[1]
        self.start_hub["x"] = parts[2]
        self.start_hub["y"] = parts[3]
        self._validate_coordinates(
            self.start_hub["x"], self.start_hub["y"], self.start_hub["name"])
        if "color=" in line:
            self.start_hub["color"] = line.split("color=")[1].split()[
                0].replace("]", "")

    def _parse_end_hub(self, line: str):
        parts = line.split()
        self.end_hub["name"] = parts[1]
        self.end_hub["x"] = parts[2]
        self.end_hub["y"] = parts[3]
        self._validate_coordinates(
            self.end_hub["x"], self.end_hub["y"], self.end_hub["name"])
        if "color=" in line:
            self.end_hub["color"] = line.split("color=")[1].split()[
                0].replace("]", "")

    def _parse_hub(self, line: str):
        hub = {}
        example = line.split("hub:")[1].split()
        name, hubx, huby, *rest = example
        hub["name"] = name
        hub["x"] = hubx
        hub["y"] = huby
        self._parse_hub_attributes(hub, rest)
        self.hubs.append(hub)

    def parse(self, context: str) -> tuple[dict, dict, list]:
        self.reset()

        for line in context:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "start_hub:" in line:
                self._parse_start_hub(line)
            elif "end_hub:" in line:
                self._parse_end_hub(line)
            elif "hub:" in line:
                self._parse_hub(line)

        return (self.start_hub, self.end_hub, self.hubs)


def parsing_hub(context: str) -> tuple[dict, dict, list]:
    return HubParser().parse(context)
