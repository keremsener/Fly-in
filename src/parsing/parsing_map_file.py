# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_map_file.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/16 14:28:20 by ksener          #+#    #+#               #
#  Updated: 2026/11/16 14:35:18 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from argparse import ArgumentParser
def parsing_map_file() -> str:
    parser = ArgumentParser()
    parser.add_argument('--map', type=str,
                        default="maps/subject_map.txt")

    args = parser.parse_args()
    return args.map