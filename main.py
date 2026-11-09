# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:45:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 14:57:03 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import parsing_hub_func, parsing_connection
from src.error import ParsingError

if __name__ == "__main__":
    try:
        hubs = parsing_hub_func("map.txt")
        all_connections = parsing_connection("map.txt")

        print("Parsed hubs:")
        for index, hub in enumerate(hubs, start=1):
            print(f"{index}. {hub}")

        print("All parsed connections:")
        for index, connection in enumerate(all_connections, start=1):
            print(f"{index}. {connection}")
    except ParsingError as error:
        print(f"Parsing error: {error}")
