from math import cos, pi, sin
from pathlib import Path

import matplotlib.pyplot as plt

# Geometria (jednostka = szerokość jednego toru)
STRAIGHT = 6           # długość prostej (tor 20×14 ≈ proporcje A4)
INNER_RADIUS = 3       # promień krawężnika
LANES = 4              # tor 0 = wewnętrzny
STRAIGHT_CELLS = 6     # pola na jednej prostej (liczba parzysta: start/meta w połowie)
BEND_CELLS = 9         # pola na jednym łuku toru 0; każdy tor dalej od środka +1

# Napisy w polach: (tor, numer pola licząc od startu, tekst)
LABELS = [
    # (0, 4, 'TURBO'),
    # (1, 17, 'UPADEK'),
    # (2, 28, 'AWARIA'),
    # (3, 10, '+2 PKT'),
]


def point(radius, section, f):
    """Punkt na torze; f od 0 do 1 wzdłuż odcinka, jazda przeciwnie do ruchu wskazówek zegara."""
    if section == 'bottom':
        return f * STRAIGHT, -radius
    if section == 'right':
        angle = -pi / 2 + f * pi
        return STRAIGHT + radius * cos(angle), radius * sin(angle)
    if section == 'top':
        return STRAIGHT - f * STRAIGHT, radius
    angle = pi / 2 + f * pi  # 'left'
    return radius * cos(angle), radius * sin(angle)


def cells(lane):
    """Początki pól toru (odcinek, f, długość pola w f), od linii startu."""
    bend = BEND_CELLS + lane
    s, b = 1 / STRAIGHT_CELLS, 1 / bend
    half = STRAIGHT_CELLS // 2
    return (
        [('bottom', 0.5 + k * s, s) for k in range(half)]
        + [('right', k * b, b) for k in range(bend)]
        + [('top', k * s, s) for k in range(STRAIGHT_CELLS)]
        + [('left', k * b, b) for k in range(bend)]
        + [('bottom', k * s, s) for k in range(half)]
    )


def line(ax, points, **style):
    ax.plot([p[0] for p in points], [p[1] for p in points], color='black', **style)


PAGE_W, PAGE_H = 297, 210  # A4 poziomo, mm
MARGIN = 2                 # margines strony, mm
SHIFT_X = -1               # przesunięcie rysunku w poziomie, mm (ujemne = w lewo)
fig = plt.figure(figsize=(PAGE_W / 25.4, PAGE_H / 25.4))
ax = fig.add_axes([(MARGIN + SHIFT_X) / PAGE_W, MARGIN / PAGE_H,
                   1 - 2 * MARGIN / PAGE_W, 1 - 2 * MARGIN / PAGE_H])

# Krawędzie torów: gęsto próbkowane zamknięte kontury
outline = [(sec, i / 100) for sec in ('bottom', 'right', 'top', 'left') for i in range(100)]
for i in range(LANES + 1):
    r = INNER_RADIUS + i
    pts = [point(r, sec, f) for sec, f in outline]
    line(ax, pts + pts[:1], linewidth=2 if i in (0, LANES) else 1)

# Podziały pól (na łukach promieniste) i napisy
for lane in range(LANES):
    r_in, r_out = INNER_RADIUS + lane, INNER_RADIUS + lane + 1
    lane_cells = cells(lane)
    for sec, f, _ in lane_cells[1:]:  # pole 0 zaczyna się na linii startu
        line(ax, [point(r_in, sec, f), point(r_out, sec, f)], linewidth=0.8)
    for label_lane, index, text in LABELS:
        if label_lane == lane:
            sec, f, step = lane_cells[index % len(lane_cells)]
            x, y = point(r_in + 0.5, sec, f + step / 2)
            ax.text(x, y, text, fontsize=7, fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black'))

# Start/meta i kierunek jazdy
line(ax, [point(INNER_RADIUS, 'bottom', 0.5), point(INNER_RADIUS + LANES, 'bottom', 0.5)],
     linewidth=4, linestyle='dashed')
start_x, start_y = point(INNER_RADIUS - 0.6, 'bottom', 0.5)
ax.annotate('', xy=(start_x + 1.5, start_y), xytext=(start_x, start_y),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

# Tytuł na środku murawy
ax.text(STRAIGHT / 2, 0.5, 'ŻUŻEL', fontsize=36, ha='center', va='center')

# Tor wypełnia stronę: granice osi dokładnie na zewnętrznej krawędzi
outer = INNER_RADIUS + LANES
ax.set_xlim(-outer, STRAIGHT + outer)
ax.set_ylim(-outer, outer)
ax.set_aspect('equal')
ax.axis('off')

pdf_path = Path(__file__).resolve().with_name('zuzel-claude.pdf')
fig.savefig(pdf_path, facecolor='white')
print(f'Zapisano PDF A4: {pdf_path}')
plt.show()
