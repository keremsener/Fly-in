# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_hub.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:39:15 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:12:24 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum
from typing import Any, Iterable

from src.core.error import HubParsingError

VALID_ZONES = {"normal", "blocked", "restricted", "priority"}


class HubOptions(Enum):
    """Allowed metadata keys inside hub bracket blocks."""

    ZONE = "zone"
    COLOR = "color"
    MAX_DRONES = "max_drones"


class HubParser:
    """Parser responsible for extracting start, end, and regular hubs."""

    def __init__(self) -> None:
        """Initialize parser state containers."""
        self.start_hub: dict[str, Any] = {}
        self.end_hub: dict[str, Any] = {}
        self.hubs: list[dict[str, Any]] = []
        self.reset()

    def reset(self) -> None:
        """Reset parser state before processing a new map."""
        self.start_hub = {
            "name": "",
            "x": 0,
            "y": 0,
            "color": "green",
            "neighbor": {},
        }
        self.end_hub = {
            "name": "",
            "x": 0,
            "y": 0,
            "color": "yellow",
            "neighbor": {},
        }
        self.hubs = []

    def _validate_name(self, name: str, line_num: int) -> None:
        """Ensure zone names do not contain forbidden dashes or spaces."""
        if not name or "-" in name or " " in name:
            raise HubParsingError(
                f"Line {line_num}: Invalid hub name '{name}'"
                f"(dashes forbidden)."
            )

    def _parse_int(self, value: str, field: str, line_num: int) -> int:
        """Safely convert string coordinate or capacity to integer."""
        try:
            return int(value)
        except ValueError as exc:
            raise HubParsingError(
                f"Line {line_num}: '{field}' must be an integer,"
                f"got '{value}'."
            ) from exc

    def _parse_metadata(
        self,
        hub: dict[str, Any],
        rest: list[str],
        line_num: int,
        ignore_max_drones: bool = False,
    ) -> None:
        """Parse bracketed [key=value] metadata tokens for a hub."""
        if not rest:
            return

        joined = " ".join(rest).strip()
        if not (joined.startswith("[") and joined.endswith("]")):
            raise HubParsingError(
                f"Line {line_num}: Malformed metadata brackets '{joined}'."
            )

        inner = joined[1:-1].strip()
        if not inner:
            return

        valid_keys = {option.value for option in HubOptions}
        for item in inner.split():
            if "=" not in item:
                raise HubParsingError(
                    f"Line {line_num}: Invalid metadata token '{item}'."
                )
            key, value = item.split("=", 1)
            if key not in valid_keys:
                raise HubParsingError(
                    f"Line {line_num}: Unknown hub option '{key}'."
                )
            if key == "zone":
                if value not in VALID_ZONES:
                    raise HubParsingError(
                        f"Line {line_num}: Invalid zone type '{value}'."
                    )
                hub["zone"] = value
            elif key == "color":
                if not value:
                    raise HubParsingError(
                        f"Line {line_num}: Color value cannot be empty."
                    )
                hub["color"] = value
            elif key == "max_drones":
                cap = self._parse_int(value, "max_drones", line_num)
                if cap < 1:
                    raise HubParsingError(
                        f"Line {line_num}: 'max_drones' must be positive."
                    )
                if not ignore_max_drones:
                    hub["max_drones"] = cap

    def _parse_connection_line(
        self, line: str, line_num: int
    ) -> tuple[str, str, int]:
        """Extract origin, destination, and capacity from a connection line."""
        cleaned = line.replace("connection:", "", 1).strip()
        capacity = 1

        if "[" in cleaned:
            route, extras = cleaned.split("[", 1)
            if not extras.endswith("]"):
                raise HubParsingError(
                    f"Line {line_num}: Unclosed bracket in connection."
                )
            inner = extras[:-1].strip()
            for item in inner.split():
                if not item.startswith("max_link_capacity="):
                    raise HubParsingError(
                        f"Line {line_num}: Invalid connection option '{item}'."
                    )
                cap_str = item.split("=", 1)[1]
                capacity = self._parse_int(
                    cap_str, "max_link_capacity", line_num
                )
                if capacity < 1:
                    raise HubParsingError(
                        f"Line {line_num}: 'max_link_capacity' must be >= 1."
                    )
        else:
            route = cleaned

        route = route.strip()
        if route.count("-") != 1:
            raise HubParsingError(
                f"Line {line_num}: Invalid connection syntax '{route}'."
            )
        origin, dest = route.split("-", 1)
        return (origin.strip(), dest.strip(), capacity)

    def find_neighbor(
        self,
        hub_name: str,
        conn_list: list[tuple[str, str, int]],
    ) -> dict[str, dict[str, int]]:
        """Build adjacency dictionary with link capacities for a given hub."""
        result: dict[str, dict[str, int]] = {}
        for origin, dest, capacity in conn_list:
            if hub_name == origin:
                result[dest] = {"capacity": capacity}
            elif hub_name == dest:
                result[origin] = {"capacity": capacity}
        return result

    def _parse_special_hub(
        self, line: str, prefix: str, target: dict[str, Any], line_num: int
    ) -> None:
        """Parse start_hub or end_hub line and enforce uniqueness."""
        if target["name"]:
            raise HubParsingError(
                f"Line {line_num}: Duplicate '{prefix}' definition."
            )
        content = line.split(prefix, 1)[1].split()
        if len(content) < 3:
            raise HubParsingError(
                f"Line {line_num}: '{prefix}' requires name, x, and y."
            )
        name, x_str, y_str, *rest = content
        self._validate_name(name, line_num)
        target["name"] = name
        target["x"] = self._parse_int(x_str, "x", line_num)
        target["y"] = self._parse_int(y_str, "y", line_num)
        self._parse_metadata(target, rest, line_num, ignore_max_drones=True)

    def _parse_hub(self, line: str, line_num: int) -> None:
        """Parse a standard intermediate hub definition."""
        content = line.split("hub:", 1)[1].split()
        if len(content) < 3:
            raise HubParsingError(
                f"Line {line_num}: 'hub:' requires name, x, and y."
            )
        name, x_str, y_str, *rest = content
        self._validate_name(name, line_num)
        hub: dict[str, Any] = {
            "name": name,
            "x": self._parse_int(x_str, "x", line_num),
            "y": self._parse_int(y_str, "y", line_num),
            "neighbor": {},
        }
        self._parse_metadata(hub, rest, line_num, ignore_max_drones=False)
        self.hubs.append(hub)

    def parse(
        self,
        context: Iterable[str],
    ) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
        """Parse all hubs and attach their neighbor dictionaries."""
        self.reset()
        connections: list[tuple[str, str, int]] = []
        seen_names: set[str] = set()

        for line_num, raw_line in enumerate(context, start=1):
            line = raw_line.strip()
            if not line or line.startswith(("#", "nb_drones:")):
                continue

            if line.startswith("start_hub:"):
                self._parse_special_hub(
                    line, "start_hub:", self.start_hub, line_num
                )
            elif line.startswith("end_hub:"):
                self._parse_special_hub(
                    line, "end_hub:", self.end_hub, line_num
                )
            elif line.startswith("hub:"):
                self._parse_hub(line, line_num)
            elif line.startswith("connection:"):
                connections.append(self._parse_connection_line(line, line_num))
            else:
                raise HubParsingError(
                    f"Line {line_num}: Unknown directive '{line}'."
                )

        if not self.start_hub["name"]:
            raise HubParsingError("Missing 'start_hub:' definition.")
        if not self.end_hub["name"]:
            raise HubParsingError("Missing 'end_hub:' definition.")

        all_names = [self.start_hub["name"], self.end_hub["name"]] + [
            h["name"] for h in self.hubs
        ]
        for name in all_names:
            if name in seen_names:
                raise HubParsingError(f"Duplicate hub name '{name}'.")
            seen_names.add(name)

        self.start_hub["neighbor"] = self.find_neighbor(
            self.start_hub["name"], connections
        )
        self.end_hub["neighbor"] = self.find_neighbor(
            self.end_hub["name"], connections
        )
        for hub in self.hubs:
            hub["neighbor"] = self.find_neighbor(hub["name"], connections)

        return (self.start_hub, self.end_hub, self.hubs)


def parsing_hub(
    context: Iterable[str],
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Convenience wrapper to parse hubs from an iterable of lines."""
    return HubParser().parse(context)
