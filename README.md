# Prosta czarno-biała plansza do gry (Windows)

Skrypt generuje czarno-białą planszę do gry żużlowej z owalnym torem i polami dopasowanymi do zakrętów. Każdy tor bliżej środka ma o dwa pola mniej. Po uruchomieniu skrypt zapisuje wektorowy PDF w formacie A4 poziomo i wyświetla planszę w nowym oknie.

## Instrukcja uruchomienia na Windows

1. Zainstaluj Pythona:  
   [Pobierz Python](https://www.python.org/downloads/windows/) i zainstaluj go z opcją "Add Python to PATH".

2. Otwórz wiersz polecenia (CMD) lub PowerShell.

3. Zainstaluj bibliotekę matplotlib:
    ```
    pip install matplotlib
    ```

4. Umieść plik `board.py` w wybranym katalogu.

5. Uruchom skrypt:
    ```
    python board.py
    ```

Skrypt zapisze obok `board.py` plik `zuzel-a4.pdf` i wyświetli planszę w nowym oknie.  
Przy drukowaniu wybierz papier A4, orientację poziomą i skalę 100% / „Rzeczywisty rozmiar”.
Jeśli masz problem z uruchomieniem, sprawdź czy Python i pip są dostępne z linii poleceń (`python --version`, `pip --version`).

## Zasady

Na planszy są 4 tory. Bieg trwa 4 okrążenia, a jazda odbywa się przeciwnie do ruchu wskazówek zegara. Okrążenia, zrywki i punkty zapisuje się na karcie biegu w środku planszy.

- **Start.** Zawodnicy zaczynają na polach A–D przed linią startu. Wyrzucenie 1 w pierwszym rzucie to dotknięcie taśmy, czyli cofnięcie o 2 pola.
- **Ruch.** Wykonujesz rzut k6. Przed rzutem możesz odkręcić gaz i dodać +1 albo +2. Przez pole zajęte przez rywala nie wolno przejechać, trzeba go objechać innym torem. Zmiana toru o jeden w bok kosztuje 1 pole. Na łuku zjazd w stronę krawężnika kosztuje dodatkowo 1 pole.
- **Limit na łuku.** Liczba w kółku na wejściu w łuk mówi, ile pól można przejechać na łuku w jednym ruchu bez ryzyka. Tor przy krawężniku jest krótszy, ale wolniejszy. Tor przy bandzie jest dłuższy, ale szybszy.
- **Strefa wejścia `»»`.** Dwa pola przed łukiem. Tutaj trzeba wybrać tor, którym pojedzie się przez łuk.
- **Test poślizgu.** Robisz go po przekroczeniu limitu albo po wjeździe na koleinę (pole kreskowane). Rzucasz k6 i odejmujesz liczbę pól ponad limit:
  - 4 i więcej: zawodnik utrzymał motocykl.
  - 2–3: poślizg. Wynosi go o jeden tor na zewnątrz i ruch się kończy.
  - 1 i mniej: upadek.
- **Banda.** Poślizg na torze przy bandzie zawsze kończy się upadkiem.
- **Szpryca.** Kto stoi tuż za rywalem w tym samym torze, dostaje −1 do ruchu. Każdy zawodnik ma 3 zrywki. Zrywka jednorazowo kasuje ten minus.
- **Pola zdarzeń:**
  - UPADEK: pauza 2 kolejki.
  - AWARIA i KAPEĆ: pauza 1 kolejka.
  - BŁOTO: −1 w następnym ruchu.
  - TURBO: +2 pola.
  - ZRYWKA: +1 żeton zrywki.
  - ŁAŃCUCH: koniec biegu.
  - +1 PKT i +2 PKT: punkty premiowe.
- **Punktacja biegu:** 3 – 2 – 1 – 0.

## Warianty planszy

Na początku `board.py` jest kilka gotowych zestawów `LABELS` (pola zdarzeń) i `ROUGH` (koleiny). Domyślnie włączona jest wersja podstawowa. Żeby wybrać inną, zakomentuj wersję podstawową i odkomentuj wybraną:

- **podstawowa**: kilka zdarzeń i pięć kolein,
- **z dużą liczbą zdarzeń**: zdarzenia na każdym torze i dużo kolein,
- **turniejowa**: bez losowych zdarzeń, liczą się tylko łuki i koleiny,
- **dla początkujących**: bez kolein, kilka korzystnych pól.

Trudność łuków ustawia `BEND_LIMIT`: 3 to wersja podstawowa, 4 łagodna, a 2 twarda. Jeśli napis albo koleina trafi na pole specjalne (`»»`, limit, A–D), skrypt przerwie działanie i wypisze, które pole koliduje.

## Zawartość

- `board.py` – skrypt z generacją planszy