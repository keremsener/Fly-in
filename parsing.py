# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 15:48:25 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
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
            if "color=" in line:
                start_hub["color"] = line.split("color=")[1].split()[0].replace("]", "")
                
        elif "end_hub:" in line:
            parts = line.split()
            end_hub["name"] = parts[1]
            parts_y = parts[3]
            end_hub["x"] = parts[2]
            end_hub["y"] = parts_y
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
                        raise Exception("Error")
                    hub[key] = value
                    
            hubs.append(hub)
            
    return (start_hub, end_hub, hubs)
def parsing_connection(context: str, conn_name: str, max_cap: int):
    pass

def parsing(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        print(json.dumps(parsing_hub(file), indent=4))
        file_contex = file.read()

if __name__ == "__main__":
    parsing("map.txt")