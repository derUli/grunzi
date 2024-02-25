# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen Paarhufer und erkundest einer Welt voller Rätsel,
Monster und friedlicher Zeitgenossen.
Das Spiel befindet sich noch in einem sehr frühen Zustand der Entwicklung.

## Systemvoraussetzungen

OS: Windows 10 / 11
RAM: 8 GB
CPU: Intel i3
GPU: OpenGL 3.3 kompatibel

## Was ist neu?
Der Alpha Build 006 stellt einen technologischen Neuanfang dar, welcher neue Konzepte einführt.

Die Maps sind jetzt im TMX Format und können mit dem Open-Source Map-Editor Tiled bearbeitet werden.
100 sammelbare Münzen werden zufällig auf der geladenen Map verteilt.
Kisten können durch die Gegend geschoben werden.

Totenköpfe spawnen nach und nach an zufälligen Orten.
Diese machen gebrauchen vom Sight Of Line Algorithmus und dem A*-Algorithmus, um den Hauptcharakter zu verfolgen.
Es ist zukünftig geplant, dass die Totenköpfe den Hauptcharakter mit Geschossen angreifen.
Das ist in diesem Build aber noch nicht implementiert.

Das Spiel kann in diesem Build nicht gewonnen oder verloren werden.
Man kann in dieser Version auf der noch recht leeren neuen Map frei herumlaufen.

Wenn Grunzi verletzt ist, regeneriert sich die Gesundheit jetzt automatisch.

# Spiel starten

Das Spiel kann mit einem Doppelklick auf "Grunzi.exe" gestartet werden.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  --window         Run in windowed mode
  --debug          Enable debug mode
  --width WIDTH    Window width in pixels
  --height HEIGHT  Window height in pixels
  --map MAP        Name of the map
  --silent         Mute the sound
  -v, --verbose    Make the operation more talkative

```

Wenn der Start des Spiels mit der Fehlermeldung, dass die "VCRUNTIME140.dll" fehlt, fehlschlägt, müssen Sie das
"Visual C++ Redistributable" von Microsoft installieren.

Sie können es hier herunterladen:
https://www.microsoft.com/de-de/download/details.aspx?id=48145

# Steuerung 

## Tastatur

WASD, Pfeiltasten: Bewegen
Shift: Sprinten
E: Schießen
G: Grunzen
F12: Screenshot erstellen
ESC: Menü aufrufen

## Controller

Controller werden in diesem Build leider nicht unterstützt.

# Einstellungen

In diesem Build gibt es kein Einstellungsmenü.
Es gibt jedoch einige Startparameter, die dem Spiel übbergeben werden können.