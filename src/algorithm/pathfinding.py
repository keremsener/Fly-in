# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pathfinding.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/11 12:01:04 by ksener          #+#    #+#               #
#  Updated: 2026/11/13 12:23:00 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import heapq
from typing import Any
from src.models import Drone, StartModel, EndModel, HubModel


def _unpack_hubs(hubs: list[Any]) -> tuple[StartModel, EndModel, list[HubModel]]:
    if len(hubs) < 3:
        raise ValueError(
            "Expected parsed hubs as [start_hub, end_hub, hub_list]."
        )

    start_hub = hubs[0]
    end_hub = hubs[1]
    middle_hubs = hubs[2]

    if not isinstance(middle_hubs, list):
        raise ValueError("Hub list format is invalid.")

    return start_hub, end_hub, middle_hubs


def build_drone_lookup(drones: list[Drone]) -> dict[int, Drone]:
    return {drone.id: drone for drone in drones}


def build_hub_lookup(
    start_hub: StartModel,
    end_hub: EndModel,
    normal_hubs: list[HubModel],
) -> dict[str, StartModel | EndModel | HubModel]:
    hub_lookup: dict[str, StartModel | EndModel | HubModel] = {
        start_hub.name: start_hub,
        end_hub.name: end_hub,
    }
    for hub in normal_hubs:
        hub_lookup[hub.name] = hub
    return hub_lookup


def _get_zone_cost(hub: StartModel | EndModel | HubModel) -> int:
    zone = getattr(hub, "zone", "normal")
    if zone == "restricted":
        return 2
    return 1


def _compute_dijkstra_paths(
    start_name: str,
    end_name: str,
    hub_lookup: dict[str, StartModel | EndModel | HubModel],
    max_paths: int,
) -> list[list[str]]:

    queue: list[tuple[int, int, str, list[str]]] = [
        (0, 0, start_name, [start_name])
    ]
    found_paths: list[list[str]] = []
    visit_counts: dict[str, int] = {}

    while queue and len(found_paths) < max_paths:
        cost, prio_bonus, current, path = heapq.heappop(queue)

        if current == end_name:
            if path not in found_paths:
                found_paths.append(path)
            continue

        visit_counts[current] = visit_counts.get(current, 0) + 1
        if visit_counts[current] > max_paths:
            continue

        current_hub = hub_lookup[current]
        for neighbor_name in current_hub.neighbor:
            if neighbor_name in path:
                continue

            target_hub = hub_lookup[neighbor_name]
            zone = getattr(target_hub, "zone", "normal")
            if zone == "blocked":
                continue

            step_cost = _get_zone_cost(target_hub)
            new_prio = prio_bonus - (1 if zone == "priority" else 0)
            heapq.heappush(
                queue,
                (cost + step_cost, new_prio, neighbor_name, path + [neighbor_name]),
            )

    if not found_paths:
        raise ValueError(f"No valid path found from '{start_name}' to '{end_name}'.")

    return found_paths


def _assign_paths_to_drones(
    drones: list[Drone],
    paths: list[list[str]],
) -> None:
    for idx, drone in enumerate(drones):
        selected_path = paths[idx % len(paths)]
        drone.path = list(selected_path[1:])


def _process_turn(state: dict[str, Any]) -> list[str]:
    start_name: str = state["start_hub"].name
    end_name: str = state["end_hub"].name
    hub_lookup = state["hub_lookup"]
    hub_occupancy: dict[str, int] = state["hub_occupancy"]
    link_capacities: dict[tuple[str, str], int] = state["link_capacities"]
    link_usage: dict[tuple[str, str], int] = {k: 0 for k in link_capacities}
    turn_moves: list[str] = []

    for drone in state["drones"]:
        if drone.is_finished:
            continue

        if drone.transit_turns_left > 0 and drone.transit_target:
            target_name = drone.transit_target
            link_key = tuple(sorted((drone.current_location, target_name)))

            drone.transit_turns_left = 0
            drone.transit_target = None
            drone.current_location = target_name
            drone.path.pop(0)

            link_usage[link_key] += 1
            turn_moves.append(f"D{drone.id}-{target_name}")

            if target_name == end_name:
                drone.is_finished = True
            continue

        if not drone.path:
            continue

        next_name = drone.path[0]
        next_hub = hub_lookup[next_name]
        link_key = tuple(sorted((drone.current_location, next_name)))

        if link_usage[link_key] >= link_capacities[link_key]:
            continue

        if next_name not in (start_name, end_name):
            max_drones = getattr(next_hub, "max_drones", 1)
            if hub_occupancy[next_name] >= max_drones:
                continue

        if drone.current_location not in (start_name, end_name):
            hub_occupancy[drone.current_location] -= 1

        link_usage[link_key] += 1
        target_zone = getattr(next_hub, "zone", "normal")

        if next_name not in (start_name, end_name):
            hub_occupancy[next_name] += 1

        if target_zone == "restricted":
            drone.transit_turns_left = 1
            drone.transit_target = next_name
            turn_moves.append(f"D{drone.id}-{drone.current_location}-{next_name}")
        else:
            drone.current_location = next_name
            drone.path.pop(0)
            turn_moves.append(f"D{drone.id}-{next_name}")

            if next_name == end_name:
                drone.is_finished = True

    return turn_moves


def find_shortest_paths(
    hubs: list[Any],
    all_connections: list[tuple[str, str, int]],
    drones: list[Drone],
) -> dict[str, Any]:
    start_hub, end_hub, normal_hubs = _unpack_hubs(hubs)
    hub_lookup = build_hub_lookup(start_hub, end_hub, normal_hubs)

    link_capacities: dict[tuple[str, str], int] = {
        tuple(sorted((orig, dest))): cap for orig, dest, cap in all_connections
    }
    hub_occupancy: dict[str, int] = {name: 0 for name in hub_lookup}
    hub_occupancy[start_hub.name] = len(drones)

    state: dict[str, Any] = {
        "start_hub": start_hub,
        "end_hub": end_hub,
        "hub_lookup": hub_lookup,
        "connections": all_connections,
        "link_capacities": link_capacities,
        "hub_occupancy": hub_occupancy,
        "drones": drones,
        "drone_lookup": build_drone_lookup(drones),
        "turn_logs": [],
    }

    paths = _compute_dijkstra_paths(
        start_hub.name,
        end_hub.name,
        hub_lookup,
        max_paths=len(drones),
    )
    _assign_paths_to_drones(drones, paths)

    while not all(drone.is_finished for drone in drones):
        turn_moves = _process_turn(state)
        if not turn_moves:
            raise RuntimeError("Simulation deadlocked: Drones cannot move forward.")
        state["turn_logs"].append(" ".join(turn_moves))

    return state