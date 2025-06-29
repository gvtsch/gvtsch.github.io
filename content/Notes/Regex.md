---
tags: ["Python"]
author: CKe
---

# Regex - Was sind "reguläre Ausdrücke"?

Reguläre Ausdrücke in Python sind sehr mächtig, können anfangs aber etwas verwirrend sein. Ein Grund es mir selber zu notieren.

## Was sind reguläre Ausdrücke?

Man kann sich Regex wie eine spezielle Sprache vorstellen, mit der man Textmuster definieren kann. Damit kann man dann z.B. in Texten nach Mustern anstelle von exakten Worten suchen. Anstatt beispielsweise in Texten nach exakten Emails oder Telefonnummern zu suchen, kann man so nach _allen Telefonnummern_ oder _allen Email-Adressen_ suchen. Das wird gleich in einem Beispiel noch klarer.

Sie werden für Aufgaben, wie Suchen, Ersetzen oder Validieren von Texten verwendet.

## Warum sind sie so nützlich?

* **Komplexe Suchen**: Texte suchen und finden, die nicht genau gleich dem Suchauftrag sind, sondern einem Muster entsprechen.
* **Datenextraktion**: Man kann spezifische Informationen aus großen Textmengen heraus ziehen (wie z.B. alle Telefonnummern).
* **Datenvalidierung**: Überprüfen, ob eine Eingabe einem bestimmten Format entspricht (ob beispielsweise eine Email-Adresse gültig ist).
* **Textbearbeitung**: Finden und ersetzen von Mustern im Text.

## Regex in Python: `re`-Modul

Python hat ein eingebautes Modul, genannt `re`, das die Arbeit mit regulären Ausdrücken ermöglicht. 

Die vermutlich wichtigsten Funktionen sind:
* **`re.search()`**: Sucht nach dem **ersten** Vorkommen eines Musters in einer Zeichenkette und gibt ein sogenanntes Match-Objekt zurück, wenn es gefunden wurde, sonst `None`.
* **`re.match()`**: Sucht nach einem Muster **am Anfang** einer Zeichenkette. Funktioniert ähnlich wie `re.search()`, ist aber etwas beschränkter.
* **`re.findall()`**: Findet alle **Vorkommen** eines Musters in einer Zeichenkette und gibt eine Liste von Zeichenketten zurück.
* **`re.sub()`**: Ersetzt Vorkommen eines Musters durch eine andere Zeichenkette.
* **`re.split()`**: Teilt eine Zeichenkette anhand eines Musters.
* **`re.compile()`**: Kompiliert ein Regex-Muster, um die Leistung zu verbessern, wenn man das gleiche Muster mehrmals verwendet. 

## Grundlegende Regex-Syntax 

Im folgenden liste ich ein paar der vielleicht gebräuchlichsten Elemente, die man Regex-Mustern finden wird.

### Literale Zeichen

Die meisten Zeichen passen sich selbst an.
* `a`: Sucht nach dem Buchstaben `a`
* `Hallo`: Sucht nach der gesamten Zeichenkette `Hallo`

### Metazeichen - Zeichen, die eine spezielle Bedeutung haben

* `.`: Passt auf jedes einzelne Zeichen (außer Newline)
  * `a.b` passt z.B. zu `abc`, `a2l`, ...
* `*`: Passt zu keiner oder mehreren Wiederholungen des vorhergehenden Zeichens oder der vorhergehenden Gruppe
  * `a*` passt z.B. zu ` `, `a`, `aa`, `abc`, ...
  * `ab*c` passt z.B. zu `ac`, `abc`, `abbbc`, ...
* `+`: Passt auf eine oder meherere Wiederholungen des vorhergehenden Zeichens oder der vorhergehenden Gruppe
  * `a+`: Passt auf `a`, `aa`, `aaa`, ... aber eben **nicht** wie `a*` zu ` `
  * `ab+c`: Passt auf `abc`, `abbc`, ... aber eben **nicht** wie `ab*c` zu `ac`
* `?`: Passt zu keiner oder einer Wiederholung des vorhergehenden Zeichens oder vorherigen Gruppe (macht es optional).
  * `colou?r`: Passt zu `color` und `colour` und deckt so in diesem Fall die unterschiedlichen Schreibweisen ab.
* `[]`: Passt zu einem einzigem Zeichen, das in den Klammern aufgeführt ist.
  * `[abc]`: Passt zu `a`, `b` oder `c`
  * `[0-9]`: Passt zu jeder Ziffer von `0` bis `9`
  * `[a-z]`: Passt zu jedem Kleinbuchstaben
  * `[A-Z]`: Passt zu jedem Großbuchstaben
  * `[a-zA-Z0-9]`: Passt zu jedem alphanumerischem Zeichen
  * `[^abc]`: Passt zu jedem Zeichen, das **nicht** `a`, `b` oder `c` ist
* `\`: Entfernt Metazeichen, so dass sie als Literale behandelt werden. Wird auch für spezielle Sequenzen verwendet.
  * `\.`: Passt zu einem tatsächlichen Punkt (`.` würde, wie oben beschrieben, keinen Punkt finden)
  * `\$`: Passt zu jedem tatsächlichen Dollarzeichen

### Spezielle, häufige verwendete Sequenzen

* `\d`: Findet/Passt zu jeder Ziffer `0` bis `9` (analog zu `[0-9]`)
* `\D`: Passt zu jedem Nicht-Ziffernzeichen
* `\w`: Passt zu jedem Schriftzeichen (alphanumerische Zeichen und Untertrisch) (analog zu `[a-zA-Z0-9_]`)
* `\W`: Passt zu jedem Nicht-Schriftzeichen
* `\s`: Passt zu jedem Leerzeichen (das schließt neben Leerzeichen auch Tabulator, Newline usw. ein)
* `\S`: Passt zu jedem Nicht-Leerzeichen
* `\b`: Passt zu einer Wortgrenze. Das ist die Position zwischen einem Schriftzeichen (`\w`) und einem Nicht-Schriftzeichen (`\W`), oder zwischen einem Wortzeichen und dem Anfang/Ende einer Zeichenkette.
  * `\bHund\b`: Passt zu `Hund` wie in `Der Hund frisst`, aber nicht zu `hundemüde`.
* `\B`: Passt zu einer Nicht-Wortgrenze, ist das Gegenteil von `\b` und passt überall dort, wo `\b` nicht passen würde.
  * `\BHund\B`: Passt nicht zu `Hund`, findet aber sehr wohl `emüde` in `Hundemüde`.
* `^`: Passt zum Anfang einer Zeichenkett
  * `^Hallo`: Passt zu `Hallo Welt`, aber nicht etwa zu `Oh, Hallo Welt`
* `$`: Passt zu dem Ende einer Zeichenkette.
  * `Welt$`: Passt zu `Hallo Welt` aber nicht zu `Die Welt ist schön`
* `|`: Logisches ODER
  * `katze|hund`: Passt zu `katze` oder `hund`
* `()`: Gruppieren von Mustern. Ermöglicht es, Operationen auf eine Gruppe anzuwenden oder Teile des Treffers zu extrahieren.
  * `(ab)+`: Passt zu `ab`, `abab`, `ababab` , ...

## Beispiele

Ich denke an einem Beispiel wird es deutlicher.

```python
import re

text = "Hallo Welt, ich bin ein Entwickler. Meine E-Mail ist test@example.com und meine Telefonnummer ist 12-345-6789."

# Beispiel 1: re.search() - Finde das erste Vorkommen
match = re.search(r"Entwickler", text)
if match:
    print(f"Gefunden: '{match.group()}' an Position {match.start()} bis {match.end()}")
    # match.group() gibt den gefundenen String zurück
    # match.start() gibt den Startindex des Treffers zurück
    # match.end() gibt den Endindex des Treffers zurück
else:
    print("Nicht gefunden.")

# Beispiel 2: re.findall() - Finde alle Vorkommen eines Musters
numbers = re.findall(r"\d+", text) # \d+ passt auf eine oder mehr Ziffern
print(f"Alle Zahlen: {numbers}")

# Beispiel 3: re.sub() - Ersetze Muster
new_text = re.sub(r"Entwickler", "Programmierer", text)
print(f"Text nach Ersetzung: {new_text}")

# Beispiel 4: E-Mail-Adresse finden (komplexeres Muster)
# r"..." ist eine "Raw String", um Backslashes nicht doppelt "escapen" zu müssen
email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
email_match = re.search(email_pattern, text)
if email_match:
    print(f"Gefundene E-Mail: {email_match.group()}")

# Beispiel 5: Telefonnummer finden (mit Gruppen)
# (\d{2}) - Gruppe 1: 2 Ziffern
# -? - optionaler Bindestrich
# (\d{3}) - Gruppe 2: 3 Ziffern
# -? - optionaler Bindestrich
# (\d{4}) - Gruppe 3: 4 Ziffern
phone_pattern = r"(\d{2})-?(\d{3})-?(\d{4})"
phone_match = re.search(phone_pattern, text)
if phone_match:
    print(f"Gefundene Telefonnummer: {phone_match.group()}")
    print(f"Vorwahl: {phone_match.group(1)}")
    print(f"Mittelteil: {phone_match.group(2)}")
    print(f"Endteil: {phone_match.group(3)}")
```

Die Ausgabe:

```bash
Gefunden: 'Entwickler' an Position 24 bis 34
Alle Zahlen: ['12', '345', '6789']
Text nach Ersetzung: Hallo Welt, ich bin ein Programmierer. Meine E-Mail ist test@example.com und meine Telefonnummer ist 12-345-6789.
Gefundene E-Mail: test@example.com
Gefundene Telefonnummer: 12-345-6789
Vorwahl: 12
Mittelteil: 345
Endteil: 6789
```
