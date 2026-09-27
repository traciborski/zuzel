# AGENTS.md

Guidance for AI coding agents working in this repository (tool-agnostic; see https://agents.md).

## Project overview

`board.py` is a standalone Python/Matplotlib script that draws a printable black-and-white speedway (żużel) board game: a stadium-shaped oval track with 4 lanes of cells, a start/finish line in the middle of the bottom straight, and optional text labels in cells. There is no package, build system, test suite, or linter.

`board-copilot.py` and `board-gemini.py` are older AI-generated variants that `board.py` replaces; don't edit or extend them.

Ignore all `*.pdf`, `*.svg`, `*.png` and `*.jpg`/`*.jpeg` files: don't read, search, edit or reference them. They are earlier drafts and generated outputs; no script reads them.

## Commands

- Install the dependency: `pip install matplotlib`
- Run: `python board.py` → writes `zuzel-a4.pdf` next to the script, then opens a preview window (`plt.show()` blocks until closed).
- Headless check: `MPLBACKEND=Agg python board.py` (PowerShell: `$env:MPLBACKEND='Agg'; python board.py`).

## Geometry (`board.py`)

- Unit = one lane width. Bend centres are at `(0, 0)` and `(STRAIGHT, 0)`; lane `n` spans radii `INNER_RADIUS + n` to `INNER_RADIUS + n + 1`. Lane 0 is the innermost.
- Constants at the top (`STRAIGHT`, `INNER_RADIUS`, `LANES`, `STRAIGHT_CELLS`, `BEND_CELLS`) are the single source of truth; derive everything else from them.
- Every point comes from `point(radius, section, f)`: `section` is `bottom`/`right`/`top`/`left`, `f` goes 0→1 along it, in racing direction (counter-clockwise). Outlines, dividers, and label positions all use it, so lines meet cleanly and dividers on bends are radial.
- `cells(lane)` lists cell starts in racing order beginning at the start line; the label cell index (`LABELS`: `(lane, cell index, text)`) counts from there and wraps around.
- Each lane has one more cell per bend than the lane inside it (two more cells in total), so each inner lane has two fewer. `STRAIGHT_CELLS` must stay even so the start line falls on a cell boundary.
- Keep the figure at A4 landscape (297×210 mm) with print margins and equal aspect; don't crop the page to the contents (no `bbox_inches='tight'`). Print at 100% / actual size.

## Language and style

- User-facing text, comments, and README are in **Polish** (title `ŻUŻEL`). Output stays black-and-white for printing.
