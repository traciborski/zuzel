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

## Zawartość

- `board.py` – skrypt z generacją planszy