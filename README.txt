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
Beim Start öffnet sich der Launcher, wo man die Einstellungen vornehmen kann.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  --window         Run in windowed mode
  --fullscreen     Run in fullscreen mode
  --debug          Enable debug mode
  --width WIDTH    Window width in pixels
  --height HEIGHT  Window height in pixels
  --map MAP        Name of the map
  --silent         Mute the sound
  --controller     Enable controller
  -v, --verbose    Make the operation more talkative
  --skip-launcher  Skip launcher

```

Wenn der Start des Spiels mit der Fehlermeldung, dass die Datei "VCRUNTIME140.dll" fehlt, fehlschlägt, muss das
"Visual C++ Redistributable" von Microsoft installiert werden.

Es ist unter folgendem Link herunterzuladen
https://www.microsoft.com/de-de/download/details.aspx?id=48145

# Steuerung

Das Spiel unterstützt Steuerung per Tastatur und per Controller.
Das Hauptmenü kann aktuell nur per Maus bedient werden.

## Tastatur

Die Steuerung über Tastatur kann im Hauptmenü unter "Hilfe & Optionen" - "Steuerung" eingesehen werden.

## Controller:

Der Controller muss bereits vor dem Spielstart mit dem Computer verbunden sein.
Um den Controller zu aktivieren, muss im Launcher die Checkbox "Controller" aktiviert, oder der Start-Parameter
--controller übergeben werden.
Wenn mehrere Controller angeschlossen sind, werden alle aktiviert.

Die Steuerung über Controller kann im Hauptmenü unter "Hilfe & Optionen" - "Steuerung" eingesehen werden.

Derzeit werden die folgenden Controller unterstützt:

* Xbox 360 Controller

Weitere Modelle können funktionieren, sind von mir aber ungetestet.

# Einstellungen

Beim Start des Spiels öffnet sich ein Dialog, wo die folgenden Einstellungen konfiguriert werden können:

* Vollbild
* Sound
* Controller
* Debug
* Bildschirmauflösung
* Map