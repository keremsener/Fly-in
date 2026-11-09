# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  models.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 11:33:45 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 11:59:01 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from pydantic import BaseModel, Field


class Hubs(BaseModel):
    name: str = Field(min_length=1)
    x: int
    y: int


class StartModel(Hubs):
    color: str = Field(default="green")


class EndModel(Hubs):
    color: str = Field(default="yellow")


class HubModel(Hubs):
    color: str = Field(default="gray")
    zone: str = Field(default="normal")
    max_drones: int = Field(default=1)


class ConnModel(BaseModel):
    origin: str
    dest: str
    max_link_cap: int = Field(default=1)