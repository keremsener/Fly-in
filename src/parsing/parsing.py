# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 16:22:51 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.models import StartModel, EndModel, HubModel
from src.error import ValidationParsingError
from .parsing_conn import ConnParser
from .parsing_hub import parsing_hub


class MapParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.start_model = None
        self.end_model = None
        self.nb_drones = 0

    def _to_models(self, hubs: list) -> list[HubModel]:
        hub_list = []
        for item in hubs:
            hub_model = HubModel(
                name=item["name"],
                x=int(item["x"]),
                y=int(item["y"]),
                color=item.get("color", "gray"),
                zone=item.get("zone", "normal"),
                max_drones=int(item.get("max_drones", 1)),
            )
            hub_list.append(hub_model)
        return hub_list

    def parse(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("nb_drones:"):
                        self.nb_drones = int(line.split(":")[1].strip())
                        if self.nb_drones < 1:
                            raise ValidationParsingError("Drone count must be a positive integer.")
                        break
                start_hub, end_hub, hubs = parsing_hub(lines)
                
                self.start_model = StartModel(
                    name=start_hub["name"],
                    x=start_hub["x"],
                    y=start_hub["y"],
                    color=start_hub["color"],
                )
                self.end_model = EndModel(
                    name=end_hub["name"],
                    x=end_hub["x"],
                    y=end_hub["y"],
                    color=end_hub["color"],
                )
                hub_list = self._to_models(hubs)
                return hub_list
            except Exception as e:
                raise ValidationParsingError(f"Map parsing failed: {e}") from e


def validate_connection(parsed_list: list[tuple[str, str, int]], file_path: str):
    seen_connections = set()
    with open(file_path, "r", encoding="utf-8") as file:
        start_hub, end_hub, hubs = parsing_hub(file)

    hub_name_set = {start_hub["name"], end_hub["name"]}
    for hub in hubs:
        hub_name_set.add(hub["name"])

    for origin, dest, max_link_cap in parsed_list:
        if origin not in hub_name_set or dest not in hub_name_set:
            return False

        if int(max_link_cap) < 1:
            return False

        connection_pair = tuple(sorted([origin, dest]))
        if connection_pair in seen_connections:
            return False

        seen_connections.add(connection_pair)

    return True

def parsing_connection(file_path: str):
    parsed_connection = ConnParser(file_path).parse_all()
    if validate_connection(parsed_connection, file_path):
        return parsed_connection
    else:
        raise ValidationParsingError(
            "Connection validation failed: unknown hub name or invalid capacity."
        )


def parsing_hub_func(file_path: str):
    return MapParser(file_path).parse()


def parsing_start_end(file_path: str):
    return MapParser(file_path).get_start_end()
