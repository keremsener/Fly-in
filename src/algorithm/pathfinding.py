# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/11 12:01:04 by ksener          #+#    #+#               #
#  Updated: 2026/11/11 12:12:30 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.models import Drone, StartModel, EndModel, HubModel


def _unpack_hubs(hubs: list) -> tuple[StartModel, EndModel, list[HubModel]]:
    if len(hubs) < 3:
        raise ValueError(
            "Expected parsed hubs as [start_hub, end_hub, hub_list].")

    start_hub = hubs[0]
    end_hub = hubs[1]
    middle_hubs = hubs[2]

    if not isinstance(middle_hubs, list):
        raise ValueError("Hub list format is invalid.")

    return start_hub, end_hub, middle_hubs


def build_drone_lookup(drones: list[Drone]) -> dict[int, Drone]:
    return {drone.id: drone for drone in drones}


def find_shortest_paths(
    hubs: list,
    all_connections: list[tuple[str, str, int]],
    drones: list[Drone],
):
    start_hub, end_hub, normal_hubs = _unpack_hubs(hubs)

    hub_lookup = {}

    hub_lookup[start_hub.name] = start_hub
    hub_lookup[end_hub.name] = end_hub

    for hub in normal_hubs:
        hub_lookup[hub.name] = hub

    state = {
        "start_hub": start_hub,
        "end_hub": end_hub,
        "hub_lookup": hub_lookup,
        "connections": all_connections,
        "drones": drones,
        "drone_lookup": build_drone_lookup(drones),
    }

    return state