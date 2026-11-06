# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  models.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 14:59:56 by ksener          #+#    #+#               #
#  Updated: 2026/11/06 16:07:55 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
from pydantic import Field, BaseModel

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