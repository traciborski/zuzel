from math import cos, pi, sin
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# Geometria (jednostka = szerokość jednego toru)
STRAIGHT = 10          # długość prostej
INNER_RADIUS = 3       # promień krawężnika
LANES = 4              # tor 0 = wewnętrzny
STRAIGHT_CELLS = 10    # pola na jednej prostej (liczba parzysta: start/meta w połowie)
BEND_CELLS = 9         # pola na jednym łuku toru 0; każdy tor dalej od środka +1

# Limit na łuku: ile pól wolno przejechać w jednym ruchu bez testu poślizgu.
# Tor 0 ma BEND_LIMIT, każdy tor dalej od środka +1.
BEND_LIMIT = 3         # podstawowa: tor 0-3 → 3, 4, 5, 6
# BEND_LIMIT = 4       # łagodna: 4, 5, 6, 7 (mniej poślizgów)
# BEND_LIMIT = 2       # twarda: 2, 3, 4, 5 (krawężnik bardzo wolny)

ENTRY_CELLS = 2        # pola strefy wejścia »» przed każdym łukiem
BANDA = 0.3            # szerokość dmuchanej bandy za torem 3

# Numery pól liczone od startu (patrz cells()); pola specjalne (»», limity, A–D)
# są zajęte, skrypt zgłosi błąd, jeśli napis lub koleina na nie trafi.

# --- Wersja podstawowa ----------------------------------------------------
# Napisy w polach: (tor, numer pola licząc od startu, tekst)
LABELS = [
    (0, 17, 'TURBO'),
    (0, 33, 'KAPEĆ'),
    (1, 17, 'UPADEK'),
    (1, 36, 'ZRYWKA'),
    (2, 28, 'AWARIA'),
    (2, 19, 'BŁOTO'),
    (3, 10, '+2 PKT'),
    (3, 37, 'TURBO'),
]
# Koleiny (luźna nawierzchnia, pola kreskowane): (tor, numer pola)
ROUGH = [(0, 28), (1, 9), (2, 31), (3, 12), (3, 13)]

# --- Wersja z dużą liczbą zdarzeń -------------------------------------------
# LABELS = [
#     (0, 1, 'BŁOTO'), (0, 9, 'UPADEK'), (0, 17, 'TURBO'), (0, 20, '+1 PKT'),
#     (0, 30, 'KAPEĆ'), (0, 34, 'ZRYWKA'),
#     (1, 7, 'AWARIA'), (1, 17, 'UPADEK'), (1, 21, 'BŁOTO'), (1, 32, 'TURBO'),
#     (1, 36, 'ZRYWKA'),
#     (2, 1, 'TURBO'), (2, 13, 'KAPEĆ'), (2, 19, 'BŁOTO'), (2, 28, 'AWARIA'),
#     (2, 38, '+1 PKT'),
#     (3, 1, 'ZRYWKA'), (3, 8, 'ŁAŃCUCH'), (3, 18, 'TURBO'), (3, 22, '+2 PKT'),
#     (3, 36, 'UPADEK'), (3, 40, 'BŁOTO'),
# ]
# ROUGH = [(0, 10), (0, 28), (1, 9), (1, 11), (1, 29), (2, 10), (2, 31),
#          (2, 32), (3, 11), (3, 12), (3, 13), (3, 33), (3, 34)]

# --- Wersja turniejowa: bez losowych zdarzeń, tylko łuki i koleiny ----------
# LABELS = []
# ROUGH = [(0, 9), (0, 28), (1, 10), (1, 30), (2, 10), (2, 31), (3, 11), (3, 33)]

# --- Wersja dla początkujących: bez kolein, kilka dobrych pól ----------------
# LABELS = [(0, 17, 'TURBO'), (1, 36, 'ZRYWKA'), (2, 19, 'TURBO'), (3, 10, '+2 PKT')]
# ROUGH = []

START_LETTERS = 'ABCD'  # pola startowe (zamiast kolorów kasków), tor 0 → A


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


def bend_starts(lane):
    """Numery pierwszych pól obu łuków toru."""
    first = STRAIGHT_CELLS // 2
    return first, first + BEND_CELLS + lane + STRAIGHT_CELLS


def special_cells(lane):
    """Pola z nadrukiem stałym: {numer pola: rodzaj}."""
    special = {len(cells(lane)) - 1: 'start'}
    for start in bend_starts(lane):
        special[start] = 'limit'
        for k in range(1, ENTRY_CELLS + 1):
            special[start - k] = 'entry'
    return special


def center(lane, index):
    sec, f, step = cells(lane)[index % len(cells(lane))]
    return point(INNER_RADIUS + lane + 0.5, sec, f + step / 2)


def cell_outline(lane, index, samples=12):
    sec, f, step = cells(lane)[index % len(cells(lane))]
    r_in, r_out = INNER_RADIUS + lane, INNER_RADIUS + lane + 1
    fs = [f + step * i / samples for i in range(samples + 1)]
    return [point(r_in, sec, g) for g in fs] + [point(r_out, sec, g) for g in reversed(fs)]


def line(ax, points, **style):
    ax.plot([p[0] for p in points], [p[1] for p in points], color='black', **style)


def boxed(ax, x, y, text, size=7, shape='round,pad=0.2', **style):
    ax.text(x, y, text, fontsize=size, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle=shape, facecolor='white', edgecolor='black'), **style)


# Kontrola: napisy i koleiny nie mogą trafiać na pola specjalne ani na siebie
used = {}
for lane, index, text in LABELS:
    used.setdefault((lane, index % len(cells(lane))), []).append(text)
for lane, index in ROUGH:
    used.setdefault((lane, index % len(cells(lane))), []).append('koleina')
for (lane, index), what in used.items():
    clash = special_cells(lane).get(index)
    if clash or len(what) > 1:
        raise SystemExit(f'Tor {lane}, pole {index}: {", ".join(what)} koliduje '
                         f'z {clash or "innym wpisem"}')

fig, ax = plt.subplots(figsize=(297 / 25.4, 210 / 25.4))  # A4 poziomo
fig.subplots_adjust(left=0.03, right=0.97, bottom=0.03, top=0.91)
ax.set_title('ŻUŻEL', fontsize=18, pad=12)

# Koleiny: kreskowane pola (pod liniami toru)
for lane, index in ROUGH:
    ax.add_patch(Polygon(cell_outline(lane, index), closed=True, fill=False, hatch='////',
                         edgecolor='black', linewidth=0))

# Krawędzie torów: gęsto próbkowane zamknięte kontury
outline = [(sec, i / 100) for sec in ('bottom', 'right', 'top', 'left') for i in range(100)]
for i in range(LANES + 1):
    r = INNER_RADIUS + i
    pts = [point(r, sec, f) for sec, f in outline]
    line(ax, pts + pts[:1], linewidth=2 if i in (0, LANES) else 1)

# Dmuchana banda: druga linia i poprzeczne kreski za ostatnim torem
r_out = INNER_RADIUS + LANES
pts = [point(r_out + BANDA, sec, f) for sec, f in outline]
line(ax, pts + pts[:1], linewidth=1)
for sec, length in (('bottom', STRAIGHT), ('right', pi * r_out),
                    ('top', STRAIGHT), ('left', pi * r_out)):
    ticks = round(length / 0.35)
    for k in range(ticks):
        f = (k + 0.5) / ticks
        line(ax, [point(r_out, sec, f), point(r_out + BANDA, sec, f)], linewidth=0.6)

# Podziały pól (na łukach promieniste), pola specjalne i napisy
for lane in range(LANES):
    r_in, r_out = INNER_RADIUS + lane, INNER_RADIUS + lane + 1
    lane_cells = cells(lane)
    for sec, f, _ in lane_cells[1:]:  # pole 0 zaczyna się na linii startu
        line(ax, [point(r_in, sec, f), point(r_out, sec, f)], linewidth=0.8)
    for index, kind in special_cells(lane).items():
        x, y = center(lane, index)
        if kind == 'limit':
            boxed(ax, x, y, str(BEND_LIMIT + lane), size=8, shape='circle,pad=0.25')
        elif kind == 'entry':
            arrow = '»' if lane_cells[index][0] == 'bottom' else '«'
            ax.text(x, y, arrow * 2, fontsize=11, fontweight='bold', ha='center', va='center')
        else:
            ax.text(x, y, START_LETTERS[lane], fontsize=10, fontweight='bold',
                    ha='center', va='center')
    for label_lane, index, text in LABELS:
        if label_lane == lane:
            x, y = center(lane, index)
            boxed(ax, x, y, text, size=6 if len(text) > 6 else 7)

# Start/meta i kierunek jazdy
line(ax, [point(INNER_RADIUS, 'bottom', 0.5), point(INNER_RADIUS + LANES, 'bottom', 0.5)],
     linewidth=4, linestyle='dashed')
start_x, start_y = point(INNER_RADIUS - 0.6, 'bottom', 0.5)
ax.annotate('', xy=(start_x + 1.5, start_y), xytext=(start_x, start_y),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(start_x + 0.75, start_y + 0.35, 'START / META', fontsize=6, ha='center', va='center')

# Murawa: legenda (lewa część) i karta biegu (prawa część)
legend_x, legend_y, row = -0.6, 2.55, 0.44
ax.text(legend_x, legend_y, 'ZASADY', fontsize=8, fontweight='bold', va='center')
rules = [
    ('limit', 'Limit na łuku: tyle pól w ruchu bez ryzyka'),
    ('entry', 'Strefa wejścia: wybierz tor przed łukiem'),
    ('rough', 'Koleiny: wjazd = test poślizgu'),
    (None, 'Ponad limit: k6 − nadwyżka → 4+ OK,'),
    (None, '2–3 poślizg (tor dalej, stop), ≤1 UPADEK'),
    (None, 'Poślizg na torze przy bandzie = UPADEK'),
    (None, 'GAZ: +1/+2 do rzutu.  Na łuku do środka: −1'),
    (None, 'SZPRYCA: tuż za rywalem −1 (zrywka kasuje)'),
    (None, 'Przez zajęte pole nie wolno przejechać'),
    (None, 'TAŚMA: 1 w pierwszym rzucie → −2 pola'),
    (None, 'UPADEK 2 kolejki, AWARIA/KAPEĆ 1, BŁOTO −1'),
    (None, 'TURBO +2 pola, ZRYWKA +1 żeton, ŁAŃCUCH koniec'),
]
for k, (icon, text) in enumerate(rules, start=1):
    y = legend_y - k * row
    if icon == 'limit':
        boxed(ax, legend_x + 0.25, y, str(BEND_LIMIT), size=6, shape='circle,pad=0.2')
    elif icon == 'entry':
        ax.text(legend_x + 0.25, y, '»»', fontsize=8, fontweight='bold', ha='center', va='center')
    elif icon == 'rough':
        ax.add_patch(Rectangle((legend_x + 0.05, y - 0.15), 0.4, 0.3, fill=False,
                               hatch='////', edgecolor='black', linewidth=0.6))
    ax.text(legend_x + (0.6 if icon else 0), y, text, fontsize=5.5, va='center')

# Karta biegu: okrążenia do odhaczania, zrywki, punkty 3-2-1-0
card_x, card_y = 6.1, 2.1
columns = [('', 0.5)] + [(str(n), 0.45) for n in range(1, 5)] + [('ZRYWKI', 1.2), ('PKT', 0.6)]
ax.text(card_x + 1.65, card_y + 0.5, 'KARTA BIEGU', fontsize=8, fontweight='bold',
        ha='center', va='center')
x = card_x
for title, width in columns:
    ax.text(x + width / 2, card_y, title, fontsize=5.5, ha='center', va='center')
    x += width
for k, letter in enumerate(START_LETTERS[:LANES], start=1):
    y = card_y - k * 0.5
    x = card_x
    for title, width in columns:
        if not title:
            ax.text(x + width / 2, y, letter, fontsize=8, fontweight='bold',
                    ha='center', va='center')
        elif title == 'ZRYWKI':
            for n in range(3):
                ax.add_patch(plt.Circle((x + 0.2 + n * 0.4, y), 0.13, fill=False, linewidth=0.6))
        else:
            ax.add_patch(Rectangle((x + 0.05, y - 0.2), width - 0.1, 0.4, fill=False,
                                   linewidth=0.6))
        x += width
ax.text(card_x + 1.65, card_y - 2.75, 'Bieg: 4 okrążenia.  Punkty: 3 – 2 – 1 – 0',
        fontsize=5.5, ha='center', va='center')

ax.set_aspect('equal')
ax.axis('off')

pdf_path = Path(__file__).resolve().with_name('zuzel-gra.pdf')
fig.savefig(pdf_path, facecolor='white')
print(f'Zapisano PDF A4: {pdf_path}')
plt.show()
