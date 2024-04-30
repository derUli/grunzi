# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen Paarhufers und erkundest einer Welt voller Action, Monster und friedlicher Zeitgenossen.

Das Spiel befindet sich noch in einem frühen Zustand der Entwicklung.
Bis jetzt ist das erste Level vollständig umgesetzt und das zweite Level befindet sich in Entwicklung.
Das fertige Spiel sollen 4 verschiedene Levels enthalten.

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

Die Tests des Linux-Build erfolgen in der WSL und einer VirtualBox Maschine.

## Was ist neu?

In diesem Build kann das bisher einzige Level abgeschlossen werden.
Ein Intro-Video, welches zur Überbrückung der Ladezeit dient, wurde hinzugefügt.
Bei jedem Spielstand wird ein friedliches Frettchen, welches bisher noch keine KI hat, zufällig auf der Karte positioniert.
Mit der Taste "F" können weitere Frettchen gespawnt werden.
Ein Spielstandsystem, welches zum Ende jedes Levels speichert, wurde hinzugefügt.
Der Launcher wurde überarbeitet.
In-Game Einstellungsmöglichkeiten wurden hinzugefügt.
Einige Bugs wurden behoben.

# Spiel starten

Das Spiel kann mit einem Doppelklick auf "Grunzi.exe" gestartet werden.
Beim Start öffnet sich der Launcher, wo man die Einstellungen vornehmen kann.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  --window              Run in windowed mode
  --fullscreen          Run in fullscreen mode
  --width WIDTH         Window width in pixels
  --height HEIGHT       Window height in pixels
  --map MAP             Name of the map
  --silent              Mute the sound
  --audio-backend {auto,xaudio2,directsound,openal,pulse,silent}
                        The audio backend
  --no-vsync            Disable V-Sync
  -v, --verbose         Make the operation more talkative
  -l, --skip-logo       Skip the logo screen and go straight to main menu
  --skip-launcher       Skip launcher


```

Wenn der Start des Spiels mit der Fehlermeldung, dass die Datei "VCRUNTIME140.dll" fehlt, fehlschlägt, muss das
"Visual C++ Redistributable" von Microsoft installiert werden.

Es ist unter folgendem Link herunterzuladen:
https://www.microsoft.com/de-de/download/details.aspx?id=48145

# Steuerung

Das Spiel unterstützt Steuerung per Tastatur und per Controller.
Das Hauptmenü kann aktuell nur per Maus bedient werden.

## Tastatur

Die Steuerung über Tastatur kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

## Controller

Der Controller muss bereits vor dem Spielstart mit dem Computer verbunden sein.
Angeschlossene Controller werden beim Spielstart automatisch erkannt.

Die Steuerung über Controller kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

Derzeit werden die folgenden Controller unterstützt:

* Xbox 360 Controller
* Rii USB Classic Controller

Weitere Modelle können funktionieren, wurden von mir aber nicht getestet.

# Einstellungen

Beim Start des Spiels öffnet sich ein Dialog, wo die folgenden Einstellungen konfiguriert werden können:

* Vollbild
* V-Sync
* Bildschirmauflösung
* Audio Backend