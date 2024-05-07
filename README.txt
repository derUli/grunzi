# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen Paarhufers und erkundest einer Welt voller Action, Monster und friedlicher Zeitgenossen.

Das Spiel befindet sich noch in einem frühen Zustand der Entwicklung.
Bis jetzt ist das erste Level vollständig umgesetzt und das zweite Level befindet sich in Entwicklung.
Das fertige Spiel sollen 4 verschiedene Levels enthalten.

## Systemvoraussetzungen

Das Spiel benötigt ein 64-Bit Windows oder Linux Betriebssystem und eine Grafikkarte,
die mindestens OpenGL 3.3 unterstützt.
Es sollte auf jeder Hardware, die in den letzten 10 Jahren auf den Markt gebracht wurde, funktionieren.
Falls es doch zu Performance-Problemen kommen sollte, kannst du die Bildschirmauflösung reduzieren.

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

In diesem Build wurden die Hühner als friedliche NPCs erneut hinzugefügt.
Rii USB Classic Controller werden jetzt unterstützt.
Teile des zweiten Levels wurden entwickelt.
Die Shader-Hintergründe im Hauptmenü wurden geändert.
Zudem wurden einige Fehler korrigiert.

# Spiel starten

Das Spiel kann mit einem Doppelklick auf "Grunzi.exe" gestartet werden.
Beim Start öffnet sich der Launcher, wo man die Einstellungen vornehmen kann.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  --window              Run in windowed mode
  --fullscreen          Run in fullscreen mode
  --borderless          Borderless window
  --width WIDTH         Window width in pixels
  --height HEIGHT       Window height in pixels
  --limit-fps LIMIT_FPS
                        Limit maximum fps
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

## Tastatur

Die Steuerung über Tastatur kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

## Controller

Angeschlossene Controller werden beim Spielstart automatisch erkannt.
Der Controller muss bereits vor dem Start des Spiels mit dem Computer verbunden sein.

Die Steuerung über Controller kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

Derzeit werden die folgenden Controller unterstützt:

* Xbox 360 Controller
* Rii USB Classic Controller

Weitere Modelle können funktionieren, wurden von mir aber nicht getestet.

# Einstellungen

Beim Start des Spiels öffnet sich ein Dialog, wo die folgenden Einstellungen konfiguriert werden können:

* Vollbild
* Rahmenlos
* V-Sync
* Bildschirmauflösung
* Audio Backend