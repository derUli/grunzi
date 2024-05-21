# Beschreibung

Im Adventure "Grunzi" übernimmst du die Rolle des gleichnamigen Paarhufers und erkundest einer Welt voller Action,
Monster und friedlicher Zeitgenossen.

Das Spiel befindet sich noch in einem frühen Zustand der Entwicklung.
Bis jetzt sind die ersten zwei Level vollständig umgesetzt und das dritte Level befindet sich in Entwicklung.
Das fertige Spiel sollen 4 verschiedene Levels enthalten.

# Systemvoraussetzungen

Das Spiel benötigt ein 64-Bit Windows oder Linux Betriebssystem und eine Grafikkarte,
die mindestens OpenGL 3.3 unterstützt.
Es sollte auf jeder Hardware, die in den letzten 10 Jahren auf den Markt gebracht wurde, funktionieren.
Falls es doch zu Performance-Problemen kommt, kannst du die Bildschirmauflösung reduzieren.

## Testsysteme

Ich teste das Spiel während der entwicklung auf meinem Desktop PC und meinem Laptop.

Im Folgenden die Hardware-Specs der beiden Systeme und die erwartete Performance.

Die erwartete Performance bezieht sich auf folgende Grafikeinstellungen und wurde mit
der RivaTuner Software gemessen.

| Einstellung         | Wert        |
|---------------------|-------------|
| Bildschirmauflösung | 1920 x 1080 |
| Vollbild            | An          |
| V-Sync              | Aus         |
| Rahmenlos           | Aus         |

### Desktop PC

| Hardware-Art    | Hersteller | Modell                 |
|-----------------|------------|------------------------|
| Prozessor       | Intel      | Core i7-10700F         |
| Grafikkarte     | NVIDIA     | GeForce GT 1030 (DDR5) |
| Arbeitsspeicher | Unbekannt  | 32 GB                  |
| Betriebssystem  | Microsoft  | Windows 11 (64-Bit)    |

**Erwartete Performance:** ⌀ 450 FPS

### Laptop

| Hardware-Art    | Hersteller | Modell              |
|-----------------|------------|---------------------|f
| Prozessor       | Intel      | Pentium Gold 7505   |
| Grafikkarte     | Intel      | UHD Graphics        |
| Arbeitsspeicher | Unbekannt  | 8 GB                |
| Betriebssystem  | Microsoft  | Windows 11 (64-Bit) |

**Erwartete Performance:** ⌀ 100 FPS

# Was ist neu?

Siehe Changelog.

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
  --silent              Mute the sound
  --audio-backend {auto,xaudio2,directsound,openal,pulse,silent}
                        The audio backend
  --antialiasing {0,2,4,8,16}
                        The antialiasing level
  --no-vsync            Disable V-Sync
  --debug               Enable OpenGL debugging
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

Derzeit werden folgende Controller unterstützt:

* Xbox 360 Controller
* Rii USB Classic Controller

Weitere Modelle können funktionieren, wurden von mir aber nicht getestet.

# Einstellungen

Das Spiel bietet die folgenden Einstellungsmöglichkeiten:

## Bildschirm

| Einstellung         | Mögliche Werte | Auswirkung auf die Performance | Im Launcher | Im Spiel |
|---------------------|----------------|--------------------------------|-------------|----------|
| Bildschirmauflösung | Systemabhängig | Hoch                           | ✓           | ✘        |
| Vollbild            | An/Aus         | Keine                          | ✓           | ✓        |
| Rahmenlos           | An/Aus         | Keine                          | ✓           | ✘        |
| V-Sync              | An/Aus         | Keine                          | ✓           | ✓        |

## Audio

| Einstellung   | Mögliche Werte                                    | Im Launcher | Im Spiel |
|---------------|---------------------------------------------------|-------------|----------|
| Audio Backend | auto, xaudio2, directsound, openal, pulse, silent | ✓           | ✘        |
| Musik         | 0 bis 100                                         | ✘           | ✓        |
| Sound         | 0 bis 100                                         | ✘           | ✓        |

## Steuerung

Hier kann die Steuerung per Tastatur und Controller eingesehen werden.
