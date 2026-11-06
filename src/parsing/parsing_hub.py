# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_hub.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:39:15 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 16:49:25 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
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
                    valid_keys = {option.value for option in HubOptions}
                    if key not in valid_keys:
                        raise Exception(
                            f"'{key}' is not match Hub options. "
                            f"Did you mean 'zone', 'color', 'max_drones'?")
                    hub[key] = value
                    
            hubs.append(hub)
            
    return (start_hub, end_hub, hubs)