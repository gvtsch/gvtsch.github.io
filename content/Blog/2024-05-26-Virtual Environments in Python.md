---
title: Virtual Environments in Python
date: 2024-05-26
tags: [Python]     # TAG names should always be lowercase
toc: true
---

In diesem Beitrag geht es darum, wie man die in Python (ab Python $3.3$) integrierten virtuellen Umgebungen nutzen kann. 

**Warum überhaupt virtuelle Umgebungen nutzen?**
Es geht unter Anderem darum, einen Ort zu haben, an dem man projekt-spezifische Pakete installieren kann. Das bezieht sich nicht nur auf die Pakete an sich, sondern auch auf deren Versionen. Nehmen wir z.B. mal an, du hast ein Projekt, welches eine spezielle, vielleicht veraltete Version eines Pakets benötigt. Wenn du nun nur eine einzelne Entwicklungsumgebung hast, wird es dir nicht möglich sein, gleichzeitig eine aktuelle Version diese Paketes für ein anderes Projekt zu nutzen. Das ist einer der Gründe, warum jedes Projekt seine eigene Umgebung mit den eigenen Paketen haben sollte.

![Bild mit drei virtuellen Entwicklungsumgebungen](https://www.dataquest.io/wp-content/uploads/2022/01/python-virtual-envs1-1024x576.webp)
_Darstellung von drei voneinander unabhängigen virtuellen Umgebungen. [Bildquelle](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/)_

**Warum venv?**
Es gibt zahlreiche andere Tools, um Environments zu verwalten. **venv** kommt allerdings mit der Standardinstallation von Python daher. Nur um eine, die wohl bekanntests, Alternative zu nennen: Anaconda.

## Erzeugen und Aktivieren einer virtuellen Umgebung
Eine gängige Praxis beim Programmieren mit Python besteht darin, virtuelle Umgebungen direkt im Projektordner zu erstellen, in dem sich auch die Python-Dateien befinden. Diese Umgebung wird üblicherweise **venv** genannt.

Man könnte folgendermaßen vorgehen: Zunächst navigiert man zu dem Ordner, in dem das Python-Projekt erstellt wurde oder erstellt werden soll. Anschließend öffnet man die Kommandozeile, dies kann beispielsweise durch Eingabe von `cmd` in der Adresszeile des Explorers erfolgen. Alternativ kann man auch innerhalb der Kommandozeile zum gewünschten Ort navigieren.

```shell
C:\***\Python_Project>python -m venv venv
```

Der Ordner mit deinem Projekt muss auch noch nicht existieren, um die Umgebung anzulegen. Dieser lässt ich einfach mit angeben.

```shell
C:\***\Python_Project>python -m venv Testing_venv\venv
```

Dieser Befehl erstellt zusätzlich den Ordner `Testing_venv`, in dem widerum der Ordner `venv` erstellt wird.

**Was passiert hier?**
Wenn du hinter `python` ein `-m` anfügst und dann ein Modul angibst, wie z.B. in `python -m venv` durchsucht dein System deine Python Umgebung nach eben jenem Modul `venv` und führt es aus. `venv` erwartet dann als nächstes einen Namen für das Environment, welches du anlegen möchtest, und legt alles benötigte für dich an. Das gewünschte Modul muss natürlich installiert, was bei `venv` mit der Standardinstallation von Python bereits der Fall ist.

Wenn du `dir` ausführst, wirst du sehen, dass ein entsprechender Ordner `venv` angelegt wurde.


```shell
C:\***\Python_Project>dir
 Datenträger in Laufwerk C: ist SYSTEM
 Volumeseriennummer: 22DA-8CAE

 Verzeichnis von C:\***\Python_Project

23.05.2024  13:09    <DIR>          .
23.05.2024  13:09    <DIR>          ..
23.05.2024  13:05    <DIR>          venv
               0 Datei(en),              0 Bytes
               3 Verzeichnis(se), 342.845.276.160 Bytes frei
```

Diese Umgebung kannst du nun mit `venv\Scripts\activate.bat` aktivieren:

```shell
C:\***\Python_Project>venv\Scripts\activate.bat

(venv) C:\***\Python_Project>
```

Natürlich kann man auch in den Ordner navigieren und das `.bat`-File manuell ausführen.

Am `(venv)` zu Beginn der Zeile kannst du nun erkennen, dass deine Umgebung aktiviert ist. Man hat nun auch die Möglichkeit Pakete zu (de-)installieren usw. Schauen wir uns zunächst mit `pip list` an, was bereits installiert ist.

```shell
(venv) C:\***\Python_Project>pip list
Package    Version
---------- -------
pip        18.1
setuptools 40.6.2
```

In diesem Python-Projekt schaue ich mir Sphinx etwas genauer an (ein separater Beitrag). Daher werde ich dieses Paket nun mit `pip install sphinx` installieren. Der Übersicht wegen erspare ich dir die Rückgabe des Install-Befehls und zeige dir stattdessen noch einmal die installierten Pakete.

```shell
(venv) C:\***\Python_Project>pip install sphinx
```

```shell
(venv) C:\***\Python_Project>pip list
Package                       Version
----------------------------- --------
alabaster                     0.7.13
Babel                         2.14.0
certifi                       2024.2.2
charset-normalizer            3.3.2
colorama                      0.4.6
docutils                      0.19
idna                          3.7
imagesize                     1.4.1
importlib-metadata            6.7.0
jinja2                        3.1.4
MarkupSafe                    2.1.5
packaging                     24.0
pip                           18.1
pygments                      2.17.2
pytz                          2024.1
requests                      2.31.0
setuptools                    40.6.2
snowballstemmer               2.2.0
sphinx                        5.3.0
sphinxcontrib-applehelp       1.0.2
sphinxcontrib-devhelp         1.0.2
sphinxcontrib-htmlhelp        2.0.0
sphinxcontrib-jsmath          1.0.1
sphinxcontrib-qthelp          1.0.3
sphinxcontrib-serializinghtml 1.1.5
typing-extensions             4.7.1
urllib3                       2.0.7
zipp                          3.15.0
```

Es wurden also die benötigten Pakete und Abhängigkeiten installiert. Im Grunde kann man nun bereits loslegen und programmieren.

## Deaktivieren und löschen
Mit `deactivate` kann man ein aktiviertes Environment wieder deaktivieren. Sollte man es gänzlich löschen wollen, löscht man entweder den gesamten Ordner von Hand oder mit `rmdir venv /s` per Kommandozeile.

```shell
C:\***\Python_Project>rmdir venv /s
Möchten Sie "venv" löschen (J/N)? J
```

Das `/s` sorgt dafür, dass der gesamte Ordner mit Unterordnern usw. gelöscht wird.

## Umgebung teilen
Wenn du mit Kollegen zusammenarbeitest und die Umgebung teilen möchtest, ist auch das möglich, wenngleich etwas weniger schön als z.B. mit Anaconda. Im Grunde  erzeugt man eine `requirements.txt`, die die Paketnamen und zugehörigen Versionen enthält.
Der Workflow der für mich am einfachsten erscheint ist:

1. `pip freeze > requirements.txt` ausführen, um eben diese Liste zu erhalten und als Textdatei abzulegen:
    ```
    (venv) C:\***\Python_Project>pip freeze
    alabaster==0.7.13
    Babel==2.14.0
    certifi==2024.2.2
    ...
    ```
2. Diese Text-Datei kann nun genutzt werden, um auf anderen Rechnern oder in anderen Umgebungen, die gelisteten Pakete mit der zugehörigen Version zu installieren. Zunächst aktiviere ich die Umgebung:
   ```shell
    C:\***\Python_Project>Testing_venv\venv\Scripts\activate.bat
    ```
    Danach installiere ich die Pakete, die in der `requirements.txt` stehen. Die Datei muss dazu in dem Ordner liegen, in dem ich mich mit der Kommandozeile gerade befinde, oder man gibt den gesamten bzw. relativen Pfad an:
    ```shell
    (venv) C:\***\Another_Python_Project>pip install -r requirements.txt    
    ```
    Es werden nun die Pakete installiert. Die Ausgabe erspare ich uns wieder. Mit `pip list` kann man das Ergebnis kontrollieren und sollte feststellen, dass dieselben Pakete wie im ursprünglichen Environment installiert wurden.

## Weitere Konventionen
Es gibt ein paar ungeschriebene Regeln beim arbeiten mit diesen virtuellen Umgebungen. 

Es versteht sich fast von selbst, aber ich erwähne es dennoch: In den Ordner mit dem virtuellen Environment haben keine anderen Dateien etwas verloren. Alle Projekt-Dateien sollten im Projektordner oder weiteren Unterordnern im Projektordner abliegen. Das Environment sollte etwas sein, dass man wegschmeißen und wieder aufbauen kann, ohne das Projekt zu beeinträchtigen.

Außerdem sollte man das Environment nicht commiten bzw. in einer Versionskontrollsoftware wie z.B. Github ablegen. Einzige Ausnahme ist die `requirements.txt`. Mit dieser Datei kann jeder das Environment selber aufbauen und es besteht einfach kein Bedarf weitere Dateien mit abzulegen.

## Environment mit Zugriff auf System-Pakete
Es besteht auch die Möglichkeit ein Environment so anzulegen, dass es auf die Pakete der System-Installation zugreifen kann.

Mit
```shell
C:\***\Python_Project>python -m venv Testing/venv --system-site-packages
```
erhält man Zugriff. Mit `Testing\venv\Scripts\activate.bat` und `pip list` kann man nun erneut kontrollieren, ob es funktioniert hat und welche Pakete im Environment vorhanden sind. 
Mit `pip list --local` kann man sich ansehen, welche Pakete man zusätzlich und ausschließlich in diesem Environment installiert hat. Die lokale Einschränkung kann man so auch für `pip freeze --local` nutzen.

Auf diese Weise werden Pakete aus der System-Installation genutzt ohne sie separat zu installieren. Mir ist kein konkreter Usecase bekannt, aber die Tatsache, dass es diese Funktion gibt, spricht dafür, dass es welche gibt.


---

Bei Fragen oder Anregungen gerne melden. 
