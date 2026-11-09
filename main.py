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

from src.parsing.parsing import parsing, parsing_connection

if __name__ == "__main__":
    hubs = parsing("map.txt")
    all_connections = parsing_connection("map.txt")

    print("Parsed hubs:")
    for index, hub in enumerate(hubs, start=1):
        print(f"{index}. {hub}")

    print("All parsed connections:")
    for index, connection in enumerate(all_connections, start=1):
        print(f"{index}. {connection}")
