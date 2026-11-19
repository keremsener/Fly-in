# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  models.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 11:33:45 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:10:32 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field


class Hubs(BaseModel):
    """Base model representing any zone/hub in the simulation graph."""

    name: str = Field(min_length=1)
    x: int
    y: int
    zone: str = Field(default="normal")
    neighbor: dict[str, dict[str, int]] = Field(default_factory=dict)


class StartModel(Hubs):
    """Model representing the unique starting hub."""

    color: str = Field(default="green")


class EndModel(Hubs):
    """Model representing the unique destination hub."""

    color: str = Field(default="yellow")


class HubModel(Hubs):
    """Model representing an intermediate network hub with capacity."""

    color: str = Field(default="gray")
    max_drones: int = Field(default=1, ge=1)


class ConnModel(BaseModel):
    """Model representing a bidirectional link between two hubs."""

    origin: str
    dest: str
    max_link_cap: int = Field(default=1, ge=1)


class Drone(BaseModel):
    """Model representing an autonomous drone and its navigation state."""

    id: int
    current_location: str
    is_finished: bool = False
    path: list[str] = Field(default_factory=list)
    transit_turns_left: int = 0
    transit_target: str | None = None


class MapGraph(BaseModel):
    """Container model representing the complete parsed network graph."""

    start_hub: StartModel
    end_hub: EndModel
    hubs: list[HubModel]
    connections: list[ConnModel]
