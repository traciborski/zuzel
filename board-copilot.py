from math import cos, pi, sin
from pathlib import Path

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(297 / 25.4, 210 / 25.4))
fig.subplots_adjust(left=0.035, right=0.965, bottom=0.045, top=0.89)

ax.set_title('ŻUŻEL', fontsize=18, pad=18)

# Wymiary planszy
cols, rows = 18, 12
straight_length = cols - rows
outer_radius = rows / 2
lane_count = 4
track_width = rows / 4
lane_width = track_width / lane_count
inner_radius = outer_radius - track_width
mid_y = rows / 2
left_center = (cols - straight_length) / 2
right_center = left_center + straight_length
straight_cells = straight_length
turn_cells = 18
outline_subdivisions = 10


def point_on_track(radius, station):
    section, position = station

    if section == 'top':
        return left_center + position * straight_length, mid_y + radius
    if section == 'right':
        angle = pi / 2 - position * pi
        return right_center + radius * cos(angle), mid_y + radius * sin(angle)
    if section == 'bottom':
        return right_center - position * straight_length, mid_y - radius
    if section == 'left':
        angle = -pi / 2 - position * pi
        return left_center + radius * cos(angle), mid_y + radius * sin(angle)
    raise ValueError(f'Unknown track section: {section}')


def stations_for_lane(lane_turn_cells):
    return (
        [('top', step / straight_cells) for step in range(straight_cells)]
        + [('right', step / lane_turn_cells) for step in range(lane_turn_cells)]
        + [('bottom', step / straight_cells) for step in range(straight_cells)]
        + [('left', step / lane_turn_cells) for step in range(lane_turn_cells)]
    )


# Kontury używają gęstszych punktów, a podziały pól własnych dla każdego toru
outline_stations = (
    [
        ('top', step / (straight_cells * outline_subdivisions))
        for step in range(straight_cells * outline_subdivisions + 1)
    ]
    + [
        ('right', step / (turn_cells * outline_subdivisions))
        for step in range(1, turn_cells * outline_subdivisions + 1)
    ]
    + [
        ('bottom', step / (straight_cells * outline_subdivisions))
        for step in range(1, straight_cells * outline_subdivisions + 1)
    ]
    + [
        ('left', step / (turn_cells * outline_subdivisions))
        for step in range(1, turn_cells * outline_subdivisions + 1)
    ]
)

# Linie poprzeczne rysuj raz; na zakrętach biegną promieniście
start_station = ('bottom', 0.5)
for lane in range(lane_count):
    outer_lane_radius = outer_radius - lane * lane_width
    inner_lane_radius = outer_lane_radius - lane_width
    lane_turn_cells = turn_cells - lane

    for station in stations_for_lane(lane_turn_cells):
        if station == start_station:
            continue
        outer_point = point_on_track(outer_lane_radius, station)
        inner_point = point_on_track(inner_lane_radius, station)
        ax.plot(
            [outer_point[0], inner_point[0]],
            [outer_point[1], inner_point[1]],
            color='black',
            linewidth=0.9,
            zorder=1,
        )

# Kontury i podziały korzystają z tych samych punktów, żeby łączyły się bez nakładania
for boundary in range(lane_count + 1):
    radius = outer_radius - boundary * lane_width
    outline = [
        point_on_track(radius, station)
        for station in outline_stations
    ]
    ax.plot(
        [point[0] for point in outline],
        [point[1] for point in outline],
        color='black',
        linewidth=2 if boundary in (0, lane_count) else 1,
        zorder=3,
    )

# Start/meta na dolnej prostej
outer_start = point_on_track(outer_radius, start_station)
inner_start = point_on_track(inner_radius, start_station)
ax.plot(
    [outer_start[0], inner_start[0]],
    [outer_start[1], inner_start[1]],
    color='black',
    linewidth=4,
    linestyle='dashed',
    marker='o',
    zorder=4,
)

ax.set_aspect('equal')
ax.set_xlim(-0.5, cols + 0.5)
ax.set_ylim(-0.5, rows + 0.5)
plt.axis('off')

pdf_path = Path(__file__).resolve().with_name('zuzel-copilot.pdf')
fig.savefig(pdf_path, format='pdf', facecolor='white')
print(f'A4 PDF saved: {pdf_path}')

plt.show()