# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:45:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 12:57:50 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import MapParser
from src.parsing.parsing_conn import ConnParser

if __name__ == "__main__":
    MapParser("map.txt").parse()
    with open("map.txt", "r", encoding="utf-8") as file:
        all_connections = ConnParser().parse_all(file)

    print("All parsed connections:")
    for index, connection in enumerate(all_connections, start=1):
        print(f"{index}. {connection}")
