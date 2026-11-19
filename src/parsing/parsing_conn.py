# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_conn.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 11:52:00 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:10:39 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.core.error import ConnectionParsingError


class ConnParser:
    """Parser responsible for extracting connection edges from map files."""

    def __init__(self, file_path: str) -> None:
        """Initialize connection parser with target file path."""
        self.origin: str = ""
        self.dest: str = ""
        self.max_link_cap: int = 1
        self.file_path: str = file_path

    def reset(self) -> None:
        """Reset current connection attributes."""
        self.origin = ""
        self.dest = ""
        self.max_link_cap = 1

    def _parse_connection(self, line: str, line_num: int) -> None:
        """Parse a single connection line and validate its capacity."""
        cleaned = line.replace("connection:", "", 1).strip()

        if "[" in cleaned:
            route, extra = cleaned.split("[", 1)
            if not extra.endswith("]"):
                raise ConnectionParsingError(
                    f"Line {line_num}: Unclosed metadata bracket."
                )
            extra = extra[:-1].strip()
            if "max_link_capacity=" in extra:
                cap_str = extra.split("max_link_capacity=", 1)[1].strip()
                try:
                    self.max_link_cap = int(cap_str)
                except ValueError as exc:
                    raise ConnectionParsingError(
                        f"Line {line_num}: Invalid capacity '{cap_str}'."
                    ) from exc
                if self.max_link_cap < 1:
                    raise ConnectionParsingError(
                        f"Line {line_num}: 'max_link_capacity' must be >= 1."
                    )
        else:
            route = cleaned

        route = route.strip()
        if route.count("-") != 1:
            raise ConnectionParsingError(
                f"Line {line_num}: Connection format is wrong."
            )

        self.origin, self.dest = route.split("-", 1)
        self.origin = self.origin.strip()
        self.dest = self.dest.strip()

    def parse_all(self) -> list[tuple[str, str, int]]:
        """Read the map file and return all parsed connection tuples."""
        connections: list[tuple[str, str, int]] = []

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line_num, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("connection:"):
                    self.reset()
                    self._parse_connection(line, line_num)
                    connections.append(
                        (self.origin, self.dest, self.max_link_cap)
                    )

        return connections
