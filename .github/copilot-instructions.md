# Copilot Instructions

## Project overview

- This is a standalone Python/Matplotlib script for drawing a black-and-white speedway board. `board.py` lays four lanes of cells around a stadium-shaped oval track, follows the bends with the cell boundaries, exports a vector A4-landscape PDF (`zuzel-a4.pdf`), and opens the result in a Matplotlib window. It does not load the other files in the repository.

## Commands

- Install the dependency: `pip install matplotlib`
- Run from the repository root: `python board.py` (displays the board and writes `zuzel-a4.pdf` beside the script)

## Code conventions

- Treat `cols`, `rows`, `straight_length`, `outer_radius`, `track_width`, `lane_count`, `turn_cells`, and `outline_subdivisions` in `board.py` as the geometry source of truth. Derive lane radii and cell positions from them when changing the layout.
- Preserve the station order around the track: top straight, right turn, bottom straight, left turn. Each lane has its own turn stations: reduce `turn_cells` by one per lane toward the infield, giving each inner lane two fewer cells overall while keeping straight-cell counts aligned. Draw each divider once and keep it radial on bends; build lane outlines from the same parametric geometry so boundaries meet cleanly without duplicate overlapping edges.
- Keep the equal aspect ratio, hidden axes, and existing view limits so the board remains legible.
- Keep the PDF page at A4 landscape size and retain safe print margins; do not crop the page to the figure contents.
- Keep the existing Polish text and documentation style: the plot title is `ŻUŻEL`, and the README and inline comments are in Polish.
