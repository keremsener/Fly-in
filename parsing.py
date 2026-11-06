# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 12:22:30 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 13:12:49 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json

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
            hub = {"name": "",
                   "x": "",
                   "y": "",
                   "zone": "",
                   "color": "",
                   "max": ""}

            name = word.split("hub:")[1].split()[0]
            hub["name"] = name
            hub["x"] = word.split("hub:")[1].split()[1]
            hub["y"] = word.split("hub:")[1].split()[2]
            if "zone" in word:
                hub["zone"] = word.split("hub:")[1].split()[3]
            if "color" in word:
                hub["color"] = word.split("hub:")[1].split()[4]
            if "max_drones" in word:
                hub["max"] = word.split("hub:")[1].split()[5]
            hubs.append(hub)
    return (start_hub, end_hub, hubs)
def parsing_connection(context: str, conn_name: str, max_cap: int):
    pass

def parsing(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        print(parsing_hub(file))
        file_contex = file.read()

if __name__ == "__main__":
    parsing("map.txt")