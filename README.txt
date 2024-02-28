# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen Paarhufers und erkundest einer Welt voller Action,
Monster und friedlicher Zeitgenossen.
Das Spiel befindet sich noch in einem sehr frühen Zustand der Entwicklung.

## Systemvoraussetzungen

Das Spiel benötigt OpenGL.

Ich habe es auf meinem Desktop PC und meinem Laptop getestet, welche folgende Specs haben.

Desktop PC:
CPU: Intel Core i7-10700F
GPU: Nvidia GeForce GT 1030
RAM: 32 GB
OS: Windows 11 64-Bit

Laptop:
CPU: Intel Pentium Gold 7505
GPU: Intel UHD Graphics
RAM: 8 GB
OS: Windows 11 64-Bit

## Was ist neu?

Der Alpha Build 006 stellt einen technologischen Neuanfang dar, welcher neue Konzepte einführt.

Die Maps sind jetzt im TMX Format und können mit dem Open-Source Map-Editor Tiled bearbeitet werden.
100 sammelbare Münzen werden zufällig auf der geladenen Map verteilt.
Kisten können durch die Gegend geschoben werden.

Totenköpfe spawnen nach und nach an zufälligen Orten.
Diese machen gebrauchen vom Sight Of Line Algorithmus und dem A*-Algorithmus, um den Hauptcharakter zu verfolgen
und auf diesen zu schießen.

Grunzi kann jetzt schießen.
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
Ctrl: Schießen
E: Benutzen
G: Grunzen
Esc: Pausenmenü öffnen
Alt + Enter: Vollbildmodus umschalten
F3: Show FPS
F12: Screenshot erstellen

## Controller

Controller werden in diesem Build leider nicht unterstützt.

# Einstellungen

In diesem Build gibt es kein Einstellungsmenü.
Es gibt jedoch einige Startoptionen, die dem Spiel übbergeben werden können.

## Grafik

Das Spiel startet mit einer Auflösung 1280x720 im Vollbildmodus, sofern keine Startoptionen übergeben wurden.
