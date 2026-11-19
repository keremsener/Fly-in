# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parsing_map_file.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ksener <ksener@student.42kocaeli.com.tr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/11/16 14:28:20 by ksener          #+#    #+#               #
#  Updated: 2026/11/19 12:12:26 by ksener          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from argparse import ArgumentParser, Namespace


def parsing_map_file() -> Namespace:
    """Parse command-line arguments supporting both positional and --map."""
    parser = ArgumentParser(description="Fly-in autonomous drone simulation.")
    parser.add_argument(
        "map_pos",
        nargs="?",
        type=str,
        default=None,
        help="Path to the map configuration file.",
    )
    parser.add_argument(
        "--map",
        type=str,
        default="maps/subject_map.txt",
        help="Path to the map configuration file (flag option).",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Render Manim visualization.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open rendered animation automatically.",
    )
    parser.add_argument(
        "--quality",
        type=str,
        default="high_quality",
        choices=["low_quality", "medium_quality", "high_quality"],
        help="Manim rendering quality.",
    )
    args = parser.parse_args()
    if args.map_pos is not None:
        args.map = args.map_pos
    return args
