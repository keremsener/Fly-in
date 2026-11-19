https://docs.manim.community/en/stable/
## Fly-in

Run the simulation:

```bash
uv run python -m src --map map.txt
```

Render the map, roads, and drone routes as an animation:

```bash
uv run python -m src --map map.txt --animate
```

Use `--preview` to open the rendered video automatically. Render quality can
be selected with `--quality low_quality`, `--quality medium_quality`, or
`--quality high_quality`.