---
tags: ["Python", "venv"]
---

# Poetry

Poetry ist ein Werkzeug für Python zur Verwaltung von Abhängigkeiten und zur Paketierung. Es ermöglicht das Deklarieren der Projektabhängigkeiten und verwaltet diese. Poetry stellt sicher, dass jeder, der an dem Projekt arbeitet, die gleichen Abhängigkeitsversionen verwendet. Es vereinfacht die Erstellung, Veröffentlichung und Verwaltung von Python-Projekten.

Ich nutze es häufiger in Projekten, die ich mit anderen teile. Dafür gibt es natürlich auch eine Lösung, die mit Python und ohne Installation zusätzlicher Pakete auskommt: 
```bash
pip install -r requirements.txt
```
Wenn man eine entsprechende Textdatei mit Paketnamen (und Versionen) hat, kann man das sicher auch lösen. Warum also dann doch `poetry`?

## Warum `Poetry` und nicht `pip install -r requirements.txt`?

`requirements.txt` hat einige Nachteile, die Poetry behebt:

* **Keine Dependency Resolution:** `requirements.txt` listet nur die direkten Abhängigkeiten auf. Poetry löst auch transitive Abhängigkeiten auf und stellt sicher, dass alle Abhängigkeiten miteinander kompatibel sind.
    * Eine transitive Abhängigkeit in Python ist eine Bibliothek, die ein Paket benötigt, das dein Projekt wiederum benötigt, ohne dass du es direkt installierst.
* **Kein Locking:** `requirements.txt` speichert keine exakten Versionen der Abhängigkeiten. Das kann zu Problemen führen, wenn neue Versionen der Abhängigkeiten veröffentlicht werden, die nicht mit dem Projekt kompatibel sind. Poetry erstellt eine `poetry.lock` Datei, die die exakten Versionen aller Abhängigkeiten speichert und so deterministische Builds gewährleistet.
* **Kein Packaging:** `requirements.txt` ist nur für die Installation von Abhängigkeiten gedacht. Poetry kann auch zum Erstellen und Veröffentlichen von Python-Paketen verwendet werden.
* **Virtual Environments:** Poetry verwaltet virtuelle Umgebungen.

Im Wesentlichen bietet Poetry ein umfassenderes und robusteres Dependency Management.

Neben den zwei genannten gibt es aber auch noch weitere Pakete und Möglichkeiten, mit denen ich mich bisher aber nicht besonders intensive beschäftigt habe:
* Pipenv
* venv/virtualenv
* pip-tools
* Hatch
* PDM
* Rye
* Conda (das wiederum ist mir auch bekannt, kann ich aber nicht überall einsetzen)

## Installation von Poetry
Poetry lässt sich wie die meisten anderen Pakete auch, über `pip` installieren.
```bash
pip install poetry
```

## Konfiguration von Poetry
Poetry bietet verschiedene Konfigurationsmöglichkeiten, um das Verhalten an die eigenen Bedürfnisse anzupassen. Die Konfiguration kann über die Datei `pyproject.toml` oder über die Kommandozeile erfolgen.

Einige wichtige Konfigurationsbereiche sind:

*   **Abhängigkeiten:** Festlegen der Projektabhängigkeiten mit Versionsbeschränkungen.
*   **Paketinformationen:** Metadaten wie Name, Version, Beschreibung, Autoren und Lizenz des Pakets.
*   **Build-Einstellungen:** Konfiguration des Build-Prozesses, z.B. welche Dateien in das Paket aufgenommen werden sollen.
* Und noch vieles, vieles mehr, wie z.B. **Virtualenv-Einstellungen**, **Repositorie** oder **Scripts**. Mit diesen habe ich mich im Kontext `Poetry` noch nicht auseinander gesetzt.

### Beispiel für eine `pyproject.toml` Datei
Hier ist nun ein Beispiel für eine Konfigurationsdatei. Sicher nicht vollständig, aber für meine Bedürfnisse vollkommen ausreichend.

```toml
[tool.poetry]
name = "meine-bibliothek"
version = "0.1.0"
description = "Eine kurze Beschreibung meiner Bibliothek."
authors = ["Dein Name <deine.email@example.com>"]
license = "MIT"
readme = "README.md"
packages = [{include = "meine_bibliothek"}]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.1"
numpy = "^1.23.4"

[tool.poetry.group.dev.dependencies]
pytest = "^7.2.0"
flake8 = "^5.0.4"
mypy = "^0.982"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Ich denke hier muss man nicht allzu zu sagen, die Datei ist relativ selbsterklärend.

## Aufsetzen eines neuen Projekts
In den nächsten Schritten geht es darum, wie man `Poetry` einsetzen kann, um ein neues Projekt aufzusetzen.

### Erstellen eines neuen Projekts
Ein neues `Poetry` Projekt erzeugt man mit **`poetry add <projektname>`. 
In der Folge wird ein neues Projektverzeichnis mit der Grundstruktur und auch der oben erwähnten `pyproject.toml`-Datei angelegt.

### Abhängigkeiten hinzufügen
Mit **`poetry add <paketname>`** oder **`poetry add <paketname>@<version>`** kann man Pakete (im letzteren Fall mit einer definierten Version) zum Projekt hinzufügen. Die werden dann auch in der `pyproject.toml` gelistet werden.

### Abhängigkeiten entfernen
Man kann natürlich auch Abhängigkeiten entfernen: **`poetry remove <paketname>`**

### Pakete aktualisieren
**`poetry update`** aktualisiert die Abhängigkeiten auf die neuesten kompatiblen Versionen, die in der `pyproject.toml` definiert sind, und aktualisiert die `poetry.lock` Datei.

### Pakete anzeigen
**`poetry show`** zeigt eine Liste aller installierten Pakete und deren Versionen an. Nützlich, um zu überprüfen, welche Versionen tatsächlich installiert sind.

### Erstellen eins Pakets
**`poetry build`** erstellt ein Paket aus dem Python-Projekt. Genauer gesagt, es erzeugt eine wheel Datei (`.whl`) und eine source archive Datei (`.tar.gz`) im dist Ordner. Diese Dateien sind die, die man dann verwenden kann, um das Paket zu verteilen oder auf PyPI zu veröffentlichen.

### Paket veröffentlichen
**`poetry publish`** dient dazu, das mit poetry build erstellte Paket (Wheel-Datei und Source-Archiv) auf einem PyPI-kompatiblen Server zu veröffentlichen, sodass andere Benutzer es installieren und verwenden können.


## Weitere nützliche Befehle und Tipps
Es gibt noch viele weitere Befehle. Ein paar werde ich noch nennen, auch wenn ich die bisher nur oberflächlich betrachtet und noch nie ernsthaft eingesetzt habe.

* **Skripte definieren**: In der `pyproject.toml` können Skripte definiert werden, die dann über `poetry run <skriptname>` ausgeführt werden können. Das ist sehr praktisch, um wiederkehrende Aufgaben zu automatisieren (z.B. Tests ausführen, Code formatieren, etc.).

    ```toml
    [tool.poetry.scripts]
    test = "pytest"
    lint = "flake8 meine_bibliothek"
    ```

    Diese Skripte können dann einfach mit `poetry run test` oder `poetry run lint` ausgeführt werden.
* **Gruppen von Abhängigkeiten**: Neben den normalen Abhängigkeiten ( `[tool.poetry.dependencies]`) und den Entwicklungsabhängigkeiten (`[tool.poetry.group.dev.dependencies]`) können auch weitere Gruppen definiert werden.  Das ist nützlich, um optionale Abhängigkeiten zu verwalten (z.B. für bestimmte Features).
* **Environment Variables**: Poetry unterstützt die Verwendung von Umgebungsvariablen in der `pyproject.toml` Datei. Das kann nützlich sein, um z.B. geheime Schlüssel oder andere sensible Informationen zu verwalten, ohne sie direkt in der Konfigurationsdatei zu speichern. 
    * Hier möchte ich auch auf [[keyring]] hinweisen.
* **Plugins**: Poetry unterstützt Plugins, um die Funktionalität zu erweitern. Es gibt eine Reihe von Community-Plugins, die z.B. die Integration mit anderen Tools verbessern oder zusätzliche Features hinzufügen.
* **Versionsverwaltung**: Poetry verwendet Semantic Versioning (SemVer). Das bedeutet, dass Versionsnummern in der Form `MAJOR.MINOR.PATCH` angegeben werden, wobei:
    *   `MAJOR`: Inkompatible API-Änderungen
    *   `MINOR`: Neue Funktionalität, abwärtskompatibel
    *   `PATCH`: Bugfixes, abwärtskompatibel
    Bei der Definition von Abhängigkeiten kann man verschiedene Versionsbeschränkungen angeben (z.B. `^1.2.3`, `~1.2.3`, `>1.2.3`, etc.).


## Zusammenfassung

Poetry ist ein mächtiges Werkzeug für das Dependency Management in Python-Projekten. Es bietet viele Vorteile gegenüber traditionellen Ansätzen wie `requirements.txt` und vereinfacht die Erstellung, Veröffentlichung und Verwaltung von Python-Paketen. Durch die Verwendung von Poetry kann man sicherstellen, dass alle Projektbeteiligten die gleichen Abhängigkeitsversionen verwenden und deterministische Builds erstellen.