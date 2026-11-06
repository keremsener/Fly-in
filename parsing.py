# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 16:27:21 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from models import Hubs, StartModel, EndModel, HubModel
from enum import Enum

class HubOptions(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"

def parsing_hub(context: str) -> tuple[dict, dict, list]:
    start_hub = {"name": "", "x": "", "y": "", "color": ""}
    end_hub = {"name": "", "x": "", "y": "", "color": ""}
    hubs = []
    
    for line in context:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "start_hub:" in line:
            parts = line.split()
            start_hub["name"] = parts[1]
            start_hub["x"] = parts[2]
            start_hub["y"] = parts[3]
            if int(start_hub["x"]) < 0 or int(start_hub["y"]) < 0:
                raise Exception("Coordinates must be a positive values.")
            if "color=" in line:
                start_hub["color"] = line.split("color=")[1].split()[0].replace("]", "")
                
        elif "end_hub:" in line:
            parts = line.split()
            end_hub["name"] = parts[1]
            parts_y = parts[3]
            end_hub["x"] = parts[2]
            end_hub["y"] = parts_y
            if int(end_hub["x"]) < 0 or int(end_hub["y"]) < 0:
                raise Exception("Coordinates must be a positive values.")
            if "color=" in line:
                end_hub["color"] = line.split("color=")[1].split()[0].replace("]", "")
                
        elif "hub:" in line:
            hub = {}
            example = line.split("hub:")[1].split()
            name, hubx, huby, *rest = example
            hub["name"] = name
            hub["x"] = hubx
            hub["y"] = huby

            for i, item in enumerate(rest):
                if i == 0:
                    if item.startswith("["):
                        item = item[1:]
                if i == len(rest) - 1:
                    if item.endswith("]"):
                        item = item[:-1]
                
                if "=" in item:
                    key, value = item.split("=")
                    if key not in HubOptions:
                        raise Exception(
                            f"'{key}' is not match Hub options. "
                            f"Did you mean 'zone', 'color', 'max_drones'?")
                    hub[key] = value
                    
            hubs.append(hub)
            
    return (start_hub, end_hub, hubs)
def parsing_connection(context: str, conn_name: str, max_cap: int):
    pass

def parsing(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            start_hub, end_hub, hubs = parsing_hub(file)
            hub_start_model = StartModel(
                name=start_hub["name"],
                x=start_hub["x"],
                y=start_hub["y"],
                color=start_hub["color"]
            )
            hub_end_model = EndModel(
                name=end_hub["name"],
                x=end_hub["x"],
                y=end_hub["y"],
                color=end_hub["color"]
            )
            hub_list = []
            for item in hubs:
                hub_model = HubModel(
                name=item["name"],
                x=int(item["x"]),
                y=int(item["y"]),
                color=item.get("color", "gray"),
                zone=item.get("zone", "normal"),
                max_drones=int(item.get("max_drones", 1))
                )
                hub_list.append(hub_model)
            print(hub_list)
        except Exception as e:
            print("Error:", e)
if __name__ == "__main__":
    parsing("map.txt")