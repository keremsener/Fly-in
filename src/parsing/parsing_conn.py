# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_conn.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 11:52:00 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 12:42:41 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.models import ConnModel


class ConnParser:
    def __init__(self):
        self.origin = ""
        self.dest = ""
        self.max_link_cap = 1

    def reset(self):
        self.origin = ""
        self.dest = ""
        self.max_link_cap = 1

    def _parse_connection(self, line: str):
        cleaned = line.replace("connection:", "", 1).strip()

        if "[" in cleaned:
            route, extra = cleaned.split("[", 1)
            extra = extra[:-1].strip() if extra.endswith("]") else extra.strip()
            if "max_link_capacity=" in extra:
                capacity = extra.split("max_link_capacity=", 1)[1].strip()
                self.max_link_cap = int(capacity)
        else:
            route = cleaned

        route = route.strip()
        if "-" not in route:
            raise Exception("Wrong format!")

        self.origin, self.dest = route.split("-", 1)
        self.origin = self.origin.strip()
        self.dest = self.dest.strip()

    def parse(self, context: str) -> tuple[str, str, int]:
        self.reset()

        for line in context:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "connection:" in line:
                self._parse_connection(line)

        return (self.origin, self.dest, self.max_link_cap)


def parsing_conn(context: str) -> tuple[str, str, int]:
    return ConnParser().parse(context)
