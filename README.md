*This project has been created as part of the 42 curriculum by ksener.*

# Fly-In

## Description

Fly-In is a Python command-line simulation of autonomous drones travelling through a network of connected hubs. Given a map, the program searches for routes from a start hub to an end hub, assigns routes to drones, schedules their moves under hub and connection capacity limits, and prints a turn-by-turn log. With animation enabled, it also renders the network and drone journeys using Manim.

The goal is to get every drone to the destination efficiently while respecting zone types and capacities. The implementation combines a bounded low-cost path search with a turn scheduler; it is a heuristic simulation, not a guarantee of a globally minimum-turn schedule for every map.

## Instructions

### Requirements and installation

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) for dependency management
- Dependencies declared by this project: Manim 0.19.1 or newer and Pydantic 2.14.3 or newer

Install and sync the project environment from the repository root:

```bash
uv sync
```

Manim rendering may require platform packages such as FFmpeg and LaTeX. Follow the [Manim installation guide](https://docs.manim.community/en/stable/installation.html) if rendering reports missing system dependencies.

### Execution

Run a simulation with a map included in this repository:

```bash
uv run python -m src --map maps/easy/01_linear_path.txt
```

The map path can also be positional:

```bash
uv run python -m src maps/easy/01_linear_path.txt
```

Render the simulation as a Manim animation:

```bash
uv run python -m src --map maps/easy/01_linear_path.txt --animate
```

Open the rendered video automatically and choose a render quality:

```bash
uv run python -m src --map maps/medium/03_priority_puzzle.txt --animate --preview --quality medium_quality
```

Available options:

| Option | Purpose |
| --- | --- |
| `MAP` | Optional positional map path; takes precedence over `--map`. |
| `--map PATH` | Select a map file. The code's default is `maps/subject_map.txt`, which is not present in this checkout; provide an existing map path. |
| `--animate` | Render the graphical simulation. Without it, only the turn log is printed. |
| `--preview` | Open the rendered animation automatically; use with `--animate`. |
| `--quality {low_quality,medium_quality,high_quality}` | Set Manim render quality. Default: `high_quality`. |
| `-h`, `--help` | Display CLI help. |

The Makefile provides `run`, `lint`, `lint-strict`, and `clean` targets. Its `run` target uses the CLI default map, so choose a direct `uv run` command above when using the maps currently in the repository. Dependencies can be installed with `uv sync`.

### Map format

Map files are UTF-8 text. Blank lines and lines beginning with `#` are ignored. The first non-comment line must declare a positive drone count. A map has one start hub, one end hub, zero or more intermediate hubs, and bidirectional connections between defined hub names.

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [zone=normal color=blue]
hub: waypoint2 2 0 [zone=normal color=blue]
end_hub: goal 3 0 [color=yellow]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Supported directives and metadata:

| Directive | Syntax | Meaning |
| --- | --- | --- |
| Drone count | `nb_drones: INTEGER` | Positive number of drones to create. |
| Start hub | `start_hub: NAME X Y [OPTIONS]` | Unique starting hub; all drones begin here. Default color: green. |
| End hub | `end_hub: NAME X Y [OPTIONS]` | Unique destination hub. Default color: yellow. |
| Intermediate hub | `hub: NAME X Y [OPTIONS]` | Regular zone. Names must be unique and cannot contain spaces or dashes. |
| Connection | `connection: HUB_A-HUB_B [max_link_capacity=INTEGER]` | Bidirectional edge. Capacity defaults to 1. Duplicate edges, self-links, and references to unknown hubs are invalid. |

Hub metadata is optional, enclosed in brackets, and separated by spaces. The parser accepts:

- `zone=normal` (default): one-turn movement cost.
- `zone=priority`: one-turn movement cost; a tie-break preference during route search.
- `zone=restricted`: two-turn route cost and a transit animation between hubs.
- `zone=blocked`: excluded from route search.
- `color=VALUE`: a color name used by the graphical renderer.
- `max_drones=INTEGER`: positive capacity for an intermediate hub. This setting is ignored for the start and end hubs.
- `max_link_capacity=INTEGER`: positive traversal capacity specified on a connection.

Coordinates must be integers. Metadata must be well-formed, and zone types must be `normal`, `priority`, `restricted`, or `blocked`.

## Algorithm and implementation

The implementation is organized into parsing, model, pathfinding/simulation, and rendering modules:

1. **Parse and validate.** The CLI selects a map. The parser reads the drone count, hub definitions and connection definitions, validates names, metadata, capacities, and references, then builds Pydantic models and adjacency data. Connections are treated as undirected.
2. **Search candidate routes.** A heap-based best-first search expands simple paths from the start. Entering a normal or priority hub costs 1; entering a restricted hub costs 2; blocked hubs are skipped. Priority hubs receive a tie-break preference. The search gathers a bounded set of distinct candidate paths, capped at 12 and also capped by the number of drones; it stops exploring beyond four cost units above the first found route.
3. **Assign routes.** Drones are assigned one at a time to the candidate path with the lowest current cost/load value. This spreads drones among candidate routes, but does not optimize a complete fleet schedule globally.
4. **Schedule turns.** Each turn, active drones are ordered with restricted-zone arrivals first, then by remaining path length and drone ID. The scheduler checks per-turn link usage and current intermediate-hub occupancy before allowing a move. When no drone can move and none is in transit, the simulation reports a deadlock rather than looping forever.
5. **Log or render.** The scheduled moves become one space-separated output line per turn. When requested, the same turn log drives the Manim scene.

Hub and drone lookup tables provide constant-time lookup by name or ID. The route search uses a heap and stores candidate paths in its queue; the number of paths is bounded, but this does not make the overall algorithm optimal or guarantee a particular complexity for every graph. The scheduler is order-based and updates occupancy while processing drones; it is not a full snapshot-based global optimizer. Route and turn choices can therefore be suboptimal, and some valid maps may be reported as deadlocked. The code does not use a graph library.

## Visual representation

Use `--animate` to generate a graphical Manim rendering. Hubs are drawn as colored circles with their names, connections as yellow lines, and drones as labeled colored squares. Drone positions advance in sync with the simulation's turn log; movement through a restricted zone is shown at the midpoint of its connection before arrival. The camera centers and scales to the hub coordinates. If `space.jpg` is available in the working directory, it is used as the background. `--quality` selects render quality and `--preview` asks Manim to open the result.

This view makes the topology, chosen paths, and congestion easier to follow than a text log alone. It is a graphical animation; the current CLI does not print colored terminal output.

## Example

Input (`maps/easy/01_linear_path.txt`):

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Command:

```bash
uv run python -m src --map maps/easy/01_linear_path.txt
```

Expected output:

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

Each line is one turn. A drone that cannot move because a capacity is full is omitted from that turn's line. In this implementation, a restricted traversal is logged as `D<ID>-<origin>-<destination>` while in transit, then as `D<ID>-<destination>` on arrival.

## Repository layout

```text
src/
  algorithm/       Candidate route search, turn scheduling, and Manim scene
  core/            Pydantic data models and parsing exceptions
  parsing/         CLI, map, hub, drone, and connection parsing
maps/              Sample maps grouped by difficulty
space.jpg           Optional animation background
```

The map catalogue is documented in [`maps/README.md`](maps/README.md).

## Resources

- Dijkstra, E. W. (1959), [“A note on two problems in connexion with graphs”](https://doi.org/10.1007/BF01386390) - foundational work on shortest paths in graphs.
- [Manim Community documentation](https://docs.manim.community/en/stable/) - scene model, animations, and rendering configuration.
- [Pydantic documentation](https://docs.pydantic.dev/latest/) - data models and field validation.
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html) - priority queue used by the route search.
- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html) - command-line argument parsing.
- [flake8 documentation](https://flake8.pycqa.org/en/latest/) and [mypy documentation](https://mypy.readthedocs.io/en/stable/) - linting and static type checking used by the Makefile targets.

### AI usage

AI assistance was used to create this README, choose the solution algorithm, and support the use of the Manim library.
