# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 15:28:00 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
from enum import Enum

class HubOptions(Enum):
    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"

def parsing_hub(context: str) -> list[dict, dict, list]:
    start_hub = {"name": "",
                 "x": "",
                 "y": "",
                 "color": ""}

    end_hub = {"name": "",
               "x": "",
               "y": "",
               "color": ""}

    hubs = []
    
    for word in context:
        if "start_hub" in word:
            name = word.split("start_hub:")[1].split()[0]
            start_hub["name"] = name
            start_hub["x"] = word.split(name)[1].split()[0]
            start_hub["y"] = word.split(name)[1].split()[1]
            start_hub["color"] = word.split("color=")[1].split()[0][:-1]
        elif "end_hub" in word:
            name = word.split("end_hub:")[1].split()[0]
            end_hub["name"] = name
            end_hub["x"] = word.split(name)[1].split()[0]
            end_hub["y"] = word.split(name)[1].split()[1]
            end_hub["color"] = word.split("color=")[1].split()[0][:-1]
        elif "hub" in word:
            hub = {}

            example = word.split("hub:")[1].split()
            name, hubx, huby, *rest = example
            hub["name"] = name
            hub["x"] = hubx
            hub["y"] = huby
            
            for i, str in enumerate(rest):
                if i == 0:
                    if str.startswith("["):
                        str = str[1:]
                    else:
                        raise Exception("Hata 1!")
                if i == len(rest) - 1:
                    if str.endswith("]"):
                        str = str[:-1]
                    else:
                        raise Exception("HATA!")
                key, value = str.split("=")
                if key not in HubOptions:
                    raise Exception("Hata 2")
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