# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 11:41:40 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.models import StartModel, EndModel, HubModel
from .parsing_hub import parsing_hub


class MapParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _to_models(self, start_hub: dict, end_hub: dict, hubs: list) -> list[HubModel]:
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
                start_hub, end_hub, hubs = parsing_hub(file)
                StartModel(
                    name=start_hub["name"],
                    x=start_hub["x"],
                    y=start_hub["y"],
                    color=start_hub["color"],
                )
                EndModel(
                    name=end_hub["name"],
                    x=end_hub["x"],
                    y=end_hub["y"],
                    color=end_hub["color"],
                )
                hub_list = self._to_models(start_hub, end_hub, hubs)
                print(hub_list)
                return hub_list
            except Exception as e:
                print("Error:", e)
                raise


def parsing_connection(context: str, conn_name: str, max_cap: int):
    pass


def parsing(file_path: str):
    return MapParser(file_path).parse()
