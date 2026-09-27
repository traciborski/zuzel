import matplotlib.pyplot as plt
import numpy as np

def draw_speedway_track_with_labels(napisy):
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Parametry geometrii
    straight_length = 10.0  # Długość prostej
    r_base = 3.0            # Promień wewnętrzny (krawężnik Toru 1)
    lane_width = 1.0        # Szerokość toru
    
    n_straight = 10         # Pola na jednej prostej
    n_arc_list = [9, 10, 11, 12]  # Pola na JEDNYM łuku (Tory 0, 1, 2, 3)
    
    # --- 1. FUNKCJA DO WYZNACZANIA ŚRODKA POLA ---
    def get_cell_center(lane, field_index):
        """
        Zwraca współrzędne (x, y) środka pola o danym indeksie na danym torze.
        Kolejność pól: Start na dolnej prostej -> Łuk Prawy -> Górna Prosta -> Łuk Lewy.
        """
        n_arc = n_arc_list[lane]
        total_fields = 2 * n_straight + 2 * n_arc
        field_index = field_index % total_fields
        
        r_mid = r_base + (lane + 0.5) * lane_width
        half_straight = n_straight // 2
        
        # Sektor 1: Dolna prosta (druga połowa, od startu do prawego łuku)
        if field_index < half_straight:
            frac = (field_index + 0.5) / half_straight
            x = straight_length / 2 + frac * (straight_length / 2)
            y = -r_mid
            return x, y
        
        field_index -= half_straight
        
        # Sektor 2: Łuk Prawy (od -pi/2 do pi/2)
        if field_index < n_arc:
            angle_start = -np.pi / 2
            angle_end = np.pi / 2
            angle = angle_start + (field_index + 0.5) * (angle_end - angle_start) / n_arc
            x = straight_length + r_mid * np.cos(angle)
            y = r_mid * np.sin(angle)
            return x, y
        
        field_index -= n_arc
        
        # Sektor 3: Górna Prosta (od prawej do lewej)
        if field_index < n_straight:
            frac = (field_index + 0.5) / n_straight
            x = straight_length - frac * straight_length
            y = r_mid
            return x, y
        
        field_index -= n_straight
        
        # Sektor 4: Łuk Lewy (od pi/2 do 3*pi/2)
        if field_index < n_arc:
            angle_start = np.pi / 2
            angle_end = 3 * np.pi / 2
            angle = angle_start + (field_index + 0.5) * (angle_end - angle_start) / n_arc
            x = 0 + r_mid * np.cos(angle)
            y = r_mid * np.sin(angle)
            return x, y
        
        field_index -= n_arc
        
        # Sektor 5: Dolna prosta (pierwsza połowa, od lewego łuku do startu)
        frac = (field_index + 0.5) / (n_straight - half_straight)
        x = 0 + frac * (straight_length / 2)
        y = -r_mid
        return x, y

    # --- 2. RYSOWANIE KRAWĘDZI TORÓW ---
    for i in range(5):
        r = r_base + i * lane_width
        ax.plot([0, straight_length], [-r, -r], color='black', lw=1.5)
        ax.plot([0, straight_length], [r, r], color='black', lw=1.5)
        
        angles_smooth = np.linspace(-np.pi/2, np.pi/2, 200)
        ax.plot(straight_length + r * np.cos(angles_smooth), r * np.sin(angles_smooth), color='black', lw=1.5)
        
        angles_smooth_left = np.linspace(np.pi/2, 3*np.pi/2, 200)
        ax.plot(0 + r * np.cos(angles_smooth_left), r * np.sin(angles_smooth_left), color='black', lw=1.5)

    # --- 3. RYSOWANIE SIATKI PÓL ---
    for lane in range(4):
        r_in = r_base + lane * lane_width
        r_out = r_in + lane_width
        n_arc = n_arc_list[lane]
        
        # Prosta Dolna i Górna
        x_straight = np.linspace(0, straight_length, n_straight + 1)
        for x in x_straight:
            ax.plot([x, x], [-r_out, -r_in], color='gray', lw=0.8, linestyle='--')
            ax.plot([x, x], [r_in, r_out], color='gray', lw=0.8, linestyle='--')
            
        # Łuk Prawy
        angles_right = np.linspace(-np.pi/2, np.pi/2, n_arc + 1)
        for a in angles_right:
            ax.plot([straight_length + r_in * np.cos(a), straight_length + r_out * np.cos(a)],
                    [r_in * np.sin(a), r_out * np.sin(a)], color='gray', lw=0.8, linestyle='--')
            
        # Łuk Lewy
        angles_left = np.linspace(np.pi/2, 3*np.pi/2, n_arc + 1)
        for a in angles_left:
            ax.plot([0 + r_in * np.cos(a), 0 + r_out * np.cos(a)],
                    [r_in * np.sin(a), r_out * np.sin(a)], color='gray', lw=0.8, linestyle='--')

    # --- 4. LINIA START / META ORAZ PODPIS ---
    meta_x = straight_length / 2
    r_top = r_base + 4 * lane_width
    
    # Podwójna wyraźna linia startowa
    ax.plot([meta_x, meta_x], [-r_top, -r_base], color='black', lw=3, linestyle='-')
    ax.plot([meta_x - 0.08, meta_x - 0.08], [-r_top, -r_base], color='white', lw=1.5, linestyle='--')
    
    # Napis START / META z ramką na środku murawy (pod dolną prostą)
    # ax.text(meta_x, -r_base + 0.5, "START / META", fontsize=11, fontweight='bold', 
    #         ha='center', va='center', color='white',
    #         bbox=dict(boxstyle='round,pad=0.5', facecolor='black', edgecolor='red', lw=2))

    # Strzałka wskazująca kierunek jazdy
    ax.annotate('', xy=(meta_x + 1.5, -r_base - 0.5), xytext=(meta_x + 0.3, -r_base - 0.5),
                arrowprops=dict(arrowstyle="->", color='black', lw=2))

    # --- 5. RYSOWANIE NAPISÓW Z LISTY ---
    for item in napisy:
        lane = item["tor"]
        field_idx = item["pole"]
        text = item["tekst"]
        
        cx, cy = get_cell_center(lane, field_idx)
        
        ax.text(cx, cy, text, fontsize=9, fontweight='bold', ha='center', va='center',
                color='black',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFD700', edgecolor='#CC9900', alpha=0.95))

    # Formatowanie
    ax.set_aspect('equal')
    plt.axis('off')
    plt.title("Żużel", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig("zuzel-gemini.pdf", bbox_inches='tight', dpi=300)
    plt.show()

# --- PRZYKŁAD UŻYCIA ---
napisy = [
    {"tor": 0, "pole": 4, "tekst": "TURBO"},
    {"tor": 1, "pole": 17, "tekst": "UPADEK"},
    {"tor": 2, "pole": 28, "tekst": "AWARIA"},
    {"tor": 3, "pole": 10, "tekst": "+2 PKT"}
]

draw_speedway_track_with_labels(napisy)