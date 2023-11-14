# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen süßen Schweinchens.
Ziel des Spiels ist es, das Ende des Levels zu erreichen.
Dabei muss die Steckdose einige Hindernisse überwinden.

Das Spiel befindet sich noch in einem frühen Stand der Entwicklung.
Bis jetzt sind nur Teile des ersten Levels spielbar.
Das fertige Spiel sollen 4 verschiedene Levels enthalten.

# Spiel starten

Das Spiel kann mit einem Doppelklick auf "Grunzi.exe" gestartet werden.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  -e, --edit            Enable in-game map editor
  -v, --debug           Enable debug loglevel
  -a, --disable-ai      Disable AI
  -d, --disable-controller
                        Disable controller support
  
```

# Steuerung 

## Tastatur

Pfeiltasten: Bewegen
E: Item benutzen
T: Item ablegen
G: Grunzen
F12: Screenshot erstellen
Shift-Taste: Rennen
ESC: Menü aufrufen
Alt-Enter: Vollbildmodus / Fenster umschalten

## Controller

Das Spiel unterstützt XBox 360 Controller.
Andere Controller können funktionieren, wurden von mir jedoch nicht getestet.
Wenn beim Start des Spiels ein Controller angeschlossen ist, wird dieser automatisch aktiviert.
Wenn mehrere Controller zeitgleich an den PC angeschlossen sind, wird nur einer davon aktiviert.

Linker Joystick oder Directional Pad: Bewegen
A: Item benutzen
Y: Item ablegen
X: Grunzen
RT: Rennen
START: Menü aufrufen

# Einstellungen

Das Spiel startet beim ersten Start in der Auflösung 1280x720 (720P) bei hoher Grafikqualität.
Dies kann in den Grafikeinstellungen geändert werden.

## Grafikqualität

Im Folgenden eine Aufschlüsselung der Grafikqualitäten:

| Qualität     | Backdrops  | Weiche Skalierung | Film Grain | Antialiasing für Fonts | Wasser-Animationen | Bloody Screen
| ------------ |:----------:|:-----------------:|:----------:|:----------------------:|:------------------:|:-------------:|
| Sehr Niedrig |     ❌    |        ❌         |     ❌     |            ❌         |         ❌        |       ❌      |
| Niedrig      |     ✅    |        ❌         |     ❌     |            ❌         |         ❌        |       ❌      |
| Mittel       |     ✅    |        ❌         |     ❌     |            ✅         |         ❌        |       ❌      |
| Hoch         |     ✅    |        ✅         |     ❌     |            ✅         |         ✅        |       ❌      |
| Sehr hoch    |     ✅    |        ✅         |     ✅     |            ✅         |         ✅        |       ✅      |
