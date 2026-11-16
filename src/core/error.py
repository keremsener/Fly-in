# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  error.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/09 15:10:00 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 14:57:05 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class ParsingError(Exception):
    pass


class HubParsingError(ParsingError):
    pass


class ConnectionParsingError(ParsingError):
    pass


class ValidationParsingError(ParsingError):
    pass
