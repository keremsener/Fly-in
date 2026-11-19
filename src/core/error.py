# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  error.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 15:10:00 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:09:40 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class ParsingError(Exception):
    """Base exception for all map parsing and validation errors."""


class HubParsingError(ParsingError):
    """Raised when hub definitions or metadata are invalid."""


class ConnectionParsingError(ParsingError):
    """Raised when connection syntax or capacities are invalid."""


class ValidationParsingError(ParsingError):
    """Raised when graph topology or global map rules fail validation."""
