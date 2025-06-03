---
tags: ["Python"]
---
# Sphinx Dokumentation erstellen
Sphinx ist ein Werkzeug zur Erstellung von Dokumentationen, insbesondere für Python-Projekte. Es ermöglicht das Generieren von ansprechenden und gut strukturierten Dokumentationen aus Docstrings und RST-Dateien. Durch die einfache Integration und Anpassbarkeit ist Sphinx eine beliebte Wahl für Entwickler. Wenn du dir schon mal die eine oder andere Dokumentation eines (z.B. Python-) Projekts angeschaut hast, bist sicher schon mal über eine mit Sphinx erzeugte Dokumentation gestolptert.

Ich selber bin bei [gym-electric-motor](https://upb-lea.github.io/gym-electric-motor/) zum ersten Mal darüber gestolpert. Hier kann man sich auch erste Eindrücke holen. Aktiv ist hier übrigens das `rtd-theme`, um das es gleich noch Mal geht.

Ich jedenfalls bin es und habe mir den Workflow zum Erzeugen der Dokmentation notiert. 
Viele Stichpunkte, nicht unbedingt viel Fließtext.

## Installation
* Zunächst aktivieren wir die Python Umgebung, in der wir das Paket installieren wollen. Dann können wir es mit `pip install Sphinx` installieren.
* Ich installiere auch immer direkt ein bestimmtes Theme: `pip install sphinx-rtd-theme`. Das gefällt mir optisch schlicht am besten.
  ![rtd Theme](https://www.writethedocs.org/_images/rtd.png)
  _Quelle: [Write the docs](https://www.writethedocs.org/guide/tools/sphinx-themes/)_
* Es gibt eine [Gallery mit Themes](https://sphinx-themes.org/), um das passende Aussehen zu wählen.

## Vorbereitung der Module
* Für jedes Modul, dass dokumentiert werden soll, muss in dem Modul eine `__init__.py` Datei angelegt sein. Die Datei kann auch leer sein und bleiben.
* Alternativ kann man die RST-Dateien, die sonst während des Prozess erzeugt würden, auch manuell erstellen.
* Klassen, Funktionen usw. sollten Docstrings haben, da diese von Sphinx automatisch erkannt und in die Dokumentation übernommen werden.
  * Ein Docstring sollte gewisee Informationen enthalten, um die folgende Dokumentation auch mit Informationen zu füllen.
  ```python
  def_function_xyz():
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
  ```

## Sphinx Quickstart
* Öffne nun eine Eingabeaufforderung oder ein Terminal Navigiere im Terminal in den Ordner, in dem die Dokumentation erzeugt werden soll.
* Führe `sphinx-quickstart` aus. Innerhalb des Terminals werden dir nun ein paar Fragen gestellt. Einfach beantworten. Falls du an deinen Antworten noch etwas ändern möchtest, ist das auch im Nachgang noch im entsprechenden Dokument möglich.    

## Erzeugung der API-Dokumentation
* Gehe zurück in den Ordner mit den Sourcen (also auf die Ebene, auf der Core, Extension usw. angezeigt wird).
* Führe `sphinx-apidoc -o DOC/sphinx_doc/ .` aus.
  * Nach `-o` folgt der Ordner, in dem die Ausgabe gespeichert werden soll.
  * `.` steht für das aktuelle Verzeichnis und alle Unterordner. Man kann aber auch einen Pfad explizit angeben.

## Konfiguration anpassen
* Öffne die `index.rst`-Datei und ergänze den `modules`-Eintrag.
* Passe die `conf.py`-Datei an:  
  * Ändere das Theme: `html_theme = 'sphinx_rtd_theme'`
  * Aktiviere Extensions: `extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]`
    * `sphinx.ext.todo` ermöglicht das Einfügen von To-Do-Listen.
    * `sphinx.ext.viewcode` ermöglicht das Anzeigen des Quellcodes.
    * `sphinx.ext.autodoc` ermöglicht das automatische Generieren der Dokumentation aus Docstrings.
    * Es gibt noch weitere Extensions, die nützlich sein könnten.
  * Füge Folgendes in die `conf.py` ein, damit Sphinx die Module findet:
  ```python
  import os
  import sys
  sys.path.insert(0, os.path.abspath(".."))
  ```

## Erstellen der Dokumentation
* Gehe zurück in den Sphinx-Doc-Ordner.
* Führe `.\make.bat html` oder `make html` aus.
  * Alternativ: `sphinx-build -M html sourcedir outputdir`
* Es wird nun im zuvor definierten Ordner das `html`-Dokument erzeugt.

## Zusammenfassung
Mit Sphinx kann man sehr schnell und einfach eine Dokumentation erzeugen, die sich auch noch interaktiv bedienen lässt. Man kann darin z.B. suchen. Wichtig ist, dass Funktionen, Klassen usw. Doc-Strings enthalten, um daraus die Dokumentation zu erzeugen. Aber diese Docstrings sind letztlich selten eine schlechte Idee, ob mit oder ohne Sphinx.
