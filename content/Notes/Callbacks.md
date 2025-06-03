---
tags: ["Python"]
author: CKe
---

# Callbacks
- Konzept ist weit verbreitete Programmiertechnik
- Ermöglicht es, eine Funktion als Argument an eine andere Funktion zu übergeben.
- Die übergebene Funktion wird dann zu einem späteren Zeitpunkt aufgerufen (z.B. als Reaktion auf ein bestimmtes Ereignis oder eine bestimmte Aktion.)

## Grundprinzipien einer Callback-Funktion
1. Definition z.B. `my_callback(message)`
   * Callback-Funktionen sind im Grunde normale Funktionen, die eine bestimmte Aufgabe ausführen. Sie werden aber nicht direkt aufgerufen, sondern an eine andere Funktion übergeben.
2. Übergeben der Callback-Funktion z.B. an `process_data(data, callback)`
   * Die Funktion, an die die Callback-Funktion übergeben wird, speichert diese und ruft die dann zu einem späteren Zeitpunkt wieder auf. Häufig wenn eine bestimmte Bedingung erfüllt ist oder ein Event eintritt.
3. Aufruf der Callback-Funktion `callback(f"Processed item: {result}")`
   * Die Callback-Funktion wird innerhalb der Funktion, die sie übernommen hat, aufgerufen. Z.B., um eine Nachricht anzuzeigen oder Daten zu verarbeiten.
  
## Beispiel

```python
def my_callback(message):
    print(f"Callback received message: {message}")

def process_data(data, callback):
    for item in data:
        # Verarbeite das Item
        result = item * 2
        # Rufe die Callback-Funktion auf und übergebe das Ergebnis
        callback(f"Processed item: {result}")

data = [1, 2, 3, 4, 5]
process_data(data, my_callback)
```

Die Augabe sollte wie folgt aussehen:

```bash
Callback received message: Processed item: 2
Callback received message: Processed item: 4
Callback received message: Processed item: 6
Callback received message: Processed item: 8
Callback received message: Processed item: 10
```

