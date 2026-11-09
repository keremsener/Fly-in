# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/06 16:45:57 by ksener          #+#    #+#               #
#  Updated: 2026/11/09 11:41:40 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.parsing.parsing import MapParser

if __name__ == "__main__":
    MapParser("map.txt").parse()
