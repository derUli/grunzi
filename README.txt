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

Wenn der Start des Spiels mit der Fehlermeldung, dass die "VCRUNTIME140.dll" fehlt, fehlschlägt, müssen Sie das
"Visual C++ Redistributable" von Microsoft installieren.

Sie können es hier herunterladen:
https://www.microsoft.com/de-de/download/details.aspx?id=48145

# Steuerung 

## Tastatur

Pfeiltasten: Bewegen
E: Item benutzen
Q: Item ablegen
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

## Video

### Bildschirm

Hier kann die Bildschirmauflösung geändert, so wie V-Sync und der Vollbildmodus ein und ausgeschaltet werden.
Nach einer Änderung der Einstellungen wird das Spiel automatisch neu gestartet, um die Änderungen zu übernehmen.

## Grafik

Hier kann man die Qualität der Grafikdetails einstellen.

**Blut**
Wenn Grunzi verletzt ist, wird der Monitor blutig eingefärbt.
**Auswirkung auf die Performance:** Mittel

**Schnee**
Hier kann der Detailgrad des Schnees eingestellt werden.
**Auswirkung auf die Performance:** Niedrig

**Nebel**
Hier kann der Nebel ein- und ausgeschaltet werden.
**Auswirkung auf die Performance:** Mittel

**Bloom**
Hier kann der Bloom-Effekt ein- und ausgeschaltet werden.
**Auswirkung auf die Performance:** Hoch

**Weiche Skalierung**
Verwende für die Skalierung der Grafiken einen Algorithmus mit Kantenglättung.

**Auswirkung auf die Performance:** Niedrig


## Audio

Hier kann die Lautstärke für Musik und Soundeffekte eingestellt werden.

## Steuerung

Hier wird die Steuerung für Tastatur und Controller angezeigt.