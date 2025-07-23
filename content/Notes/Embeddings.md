---
title: Wort- und Token-Embeddings - Die Sprache der Vektoren
date: 2025-07-22
tags: [ml, dl, python, llm, nlp, transformer]     # TAG names should always be lowercase
toc: true
---

# Wort- und Token-Embeddings - Die Sprache der Vektoren

Embeddings - ein Kernkonzept, das moderne künstliche Intelligenz in der Sprachverarbeitung antreibt. Wenn Computer Sprache verstehen sollen, müssen sie Text in ein Format umwandeln, mit dem sie arbeiten können. Hier kommen Embeddings ins Spiel: Sie sind der Schlüssel, um Wörter und deren Bedeutungen für Maschinen "begreifbar" zu machen.

## Was sind Embeddings?

Embeddings sind numerische Vektordarstellungen von Wörtern, Subwörtern oder anderen Texteinheiten, die wir als [[Tokenization|Tokens]] bezeichnen. Ihr Hauptzweck ist es, die semantische (bedeutungsbezogene) und syntaktische (grammatikalische) Beziehung zwischen diesen Tokens in einem hochdimensionalen Raum zu erfassen. Das bedeutet: Wörter mit ähnlicher Bedeutung oder Funktion liegen im Vektorraum näher beieinander.

Stell dir vor, du könntest jedes Wort nicht nur als Zeichenkette, sondern als einen Punkt in einem riesigen, mathematischen Raum darstellen. Wenn "König" und "Königin" in diesem Raum nahe beieinander liegen und "Apfel" weit entfernt ist, dann spiegelt das ihre jeweilige Bedeutungsähnlichkeit wider.

Um die Funktionsweise zu verdeutlichen, möchte ich ein vereinfachtes Beispiel nutzen.

```python
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Beispiel-Vektoren
koenig = np.array([1, 1, 0, 0])
vergleichs_vektoren = {
    "Königin": np.array([1, 1, 1, 0]),
    "Königin_2": np.array([2, 2, 0.1, 0]),
    "Königin_3": np.array([3, 3, 0.2, 0]),
    "Apfel": np.array([0, 0, 10, 10])
}
```

In diesem Codeabschnitt habe ich ein paar hypothetische Beispielvektoren definiert, die Embeddings für die Wörter _König_, _Königin_ und _Apfel_ darstellen. Zusätzlich wurden Variationen des Vektors für _Königin_ angelegt, um die Auswirkungen von Vektorgröße auf Distanzmaße zu illustrieren. Dies sind wirklich nur stark vereinfachte Beispielvektoren, um das Prinzip zu verdeutlichen.

In der Praxis haben diese Wort-Embeddings bedeutend mehr Dimensionen. Moderne Sprachmodelle wie GPT-3 nutzen beispielsweise Embeddings mit bis zu 12288 Dimensionen. Diese komplexen Embeddings werden nicht manuell erstellt, sondern während des Trainings der Sprachmodelle gelernt, indem das Modell Muster und Beziehungen in riesigen Textmengen analysiert.

### Messung der Ähnlichkeit von Embeddings

Um die semantische Ähnlichkeit zwischen Vektoren zu messen, werden verschiedene mathematische Metriken verwendet. Die Kosinus-Ähnlichkeit und das Skalarprodukt (Dot Product) sind besonders wichtig im Kontext von Natural Language Processing (NLP) und Large Language Models (LLMs), da sie die Richtung von Vektoren bewerten und somit die Bedeutungsähnlichkeit robust erfassen. Daneben gibt es Distanzmaße wie die Euklidische oder Manhattan-Distanz, die den "Abstand" zwischen Vektoren im Raum messen.

Wir werden hier die [[Kosinusaehnlichkeit|Kosinus-Ähnlichkeit]], das Skalarprodukt, die Euklidische Distanz und die Manhatten-Distanz zusammen mit der Euklidischen und Manhattan-Distanz in einem Beispiel vergleichen, um ihre Unterschiede und Zusammenhänge in der Bewertung der semantischen Nähe zu verdeutlichen.


```python
def vektor_metriken(vektor_a: np.ndarray, vektor_b: np.ndarray) -> tuple[float, float, float, float]:
    
    if not isinstance(vektor_a, np.ndarray) or not isinstance(vektor_b, np.ndarray):
        raise ValueError("vektor_a und vektor_b müssen NumPy-Arrays sein.")
    if vektor_a.shape != vektor_b.shape:
        raise ValueError("vektor_a und vektor_b müssen die gleiche Form haben.")

    # Skalarprodukt (Dot Product): Misst die "Projektion" eines Vektors auf den anderen
    dot_product = np.dot(vektor_a, vektor_b)
    
    # Kosinus-Ähnlichkeit: Misst den Cosinus des Winkels zwischen den Vektoren
    # Formel: (A . B) / (||A|| * ||B||)
    norm_a = np.linalg.norm(vektor_a)
    norm_b = np.linalg.norm(vektor_b)
    kosinus = dot_product / (norm_a * norm_b) if (norm_a * norm_b) != 0 else 0
    
    # Euklidische Distanz: Geradliniger Abstand im Vektorraum
    euklidisch = np.linalg.norm(vektor_a - vektor_b)
    # Manhattan-Distanz: Summe der absoluten Differenzen der Koordinaten (City-Block-Distanz)
    manhattan = np.linalg.norm(vektor_a - vektor_b, ord=1)
    
    return dot_product, kosinus, euklidisch, manhattan
```

Die Funktion `vektor_metriken` berechnet die besagten Metriken für je zwei gegebene Vektoren. Die folgende Funktion `vergleiche_vektoren` verwendet `vektor_metriken`, um einen Referenzvektor mit einer Reihe von Vergleichsvektoren aus einem Dictionary zu vergleichen und die Ergebnisse übersichtlich in einer Tabelle auszugeben.


```python
def vergleiche_vektoren(referenz_vektor: np.ndarray, vergleichs_vektoren_dict: dict[str, np.ndarray]) -> pd.DataFrame:

    if not isinstance(referenz_vektor, np.ndarray):
        raise ValueError("referenz_vektor muss ein NumPy-Array sein.")
    if not isinstance(vergleichs_vektoren_dict, dict):
        raise ValueError("vergleichs_vektoren_dict muss ein Dictionary sein.")

    ergebnisse = []
    for name, vektor in vergleichs_vektoren_dict.items():
        if not isinstance(vektor, np.ndarray):
            raise ValueError(f"Der Wert für '{name}' im vergleichs_vektoren_dict muss ein NumPy-Array sein.")
        dot_product, kosinus, euklidisch, manhattan = vektor_metriken(referenz_vektor, vektor)
        ergebnisse.append({
            "Vergleichs-Wort": name,
            "Skalarprodukt": dot_product,
            "Kosinus-Ähnlichkeit": kosinus,
            "Euklidische Distanz": euklidisch,
            "Manhattan-Distanz": manhattan
        })

    df = pd.DataFrame(ergebnisse)
    # Setze "Vergleichs-Wort" als Index für bessere Lesbarkeit
    df = df.set_index("Vergleichs-Wort")
    return df
```

Im folgenden vergleichen wir den Vektor `König` mit den anderen definierten Beispielvektoren und geben die berechneten Ähnlichkeitswerte aus.


```python
ergebnisse_df = vergleiche_vektoren(koenig, vergleichs_vektoren)
print(ergebnisse_df)
```
```bash
Beispiel       Apfel   Königin  Königin_2  Königin_3
Metrik                                              
Euklidisch  14.21267  1.000000   1.417745   2.835489
Kosinus      0.00000  0.816497   0.999376   0.998891
Manhattan   22.00000  1.000000   2.100000   4.200000
``` 

### Interpretation der Metriken im Kontext von Embeddings

Die Tabelle verdeutlicht die unterschiedlichen Eigenschaften der Metriken beim Vergleich des Referenzvektors für König mit den anderen Wörtern:

* Skalarprodukt (Dot Product):
    * Misst die "Übereinstimmung" der Richtungen und berücksichtigt gleichzeitig die Länge (Magnitude) der Vektoren. Ein größeres Skalarprodukt deutet auf eine stärkere Ausrichtung in dieselbe Richtung hin und/oder auf längere Vektoren.
    * Je höher der Wert, desto ähnlicher sind die Vektoren.
    * Im Beispiel: Königin_3 hat mit 6.3 das höchste Skalarprodukt zu König, gefolgt von Königin_2 (4.2) und Königin (2.0). Dies ist, wie erwartet, eine Folge ihrer zunehmenden Vektorlänge, während ihre semantische Richtung zum "König" sehr ähnlich bleibt. Apfel hat ein Skalarprodukt von 0, da die Vektoren orthogonal zueinander stehen.
* Kosinus-Ähnlichkeit:
    * Misst den Winkel zwischen Vektoren und spiegelt somit rein die semantische Richtung oder Ähnlichkeit wider, unabhängig von deren Länge.
    * Hohe Werte (nahe 1) = sehr ähnliche Bedeutung (Vektoren zeigen in fast dieselbe Richtung).
    * Niedrige Werte (nahe 0 oder -1) = geringe oder entgegengesetzte Ähnlichkeit.
    * Im Beispiel: Königin_2 (0.999) und Königin_3 (0.999) sind dem König am ähnlichsten, da ihre Vektoren fast perfekt in dieselbe Richtung zeigen. Königin (0.816) ist immer noch ähnlich, aber der zusätzliche Eintrag in der dritten Dimension (weiblich) führt zu einem etwas größeren Winkel. Apfel ist komplett unähnlich (0.000), da sein Vektor eine völlig andere Richtung hat. Die Kosinus-Ähnlichkeit ist die bevorzugte Metrik für LLMs, da sie die Bedeutungsähnlichkeit robust erfasst.
* Euklidische Distanz und Manhattan-Distanz:
    * Messen den geometrischen "Abstand" zwischen zwei Vektoren im Vektorraum.
    * Kleine Werte bedeuten hohe Ähnlichkeit (Vektoren sind nah beieinander).
    * Große Werte bedeuten geringe Ähnlichkeit (Vektoren sind weit voneinander entfernt).
    * Sie sind empfindlich gegenüber der Vektorgröße. Königin_2 und Königin_3 zeigen trotz ihrer hohen semantischen Ähnlichkeit (hohe Kosinus-Werte) eine größere Distanz zu König als Königin. Das liegt daran, dass ihre Vektoren einfach "länger" sind und somit weiter entfernt liegen, auch wenn ihre Richtung sehr ähnlich ist.
    * Diese Distanzmaße sind weniger geeignet, um rein semantische Beziehungen in Embeddings zu quantifizieren, da die Bedeutung von Wörtern in LLMs oft durch die Richtung ihrer Embeddings und weniger durch deren Länge repräsentiert wird.

## Fazit

Das Skalarprodukt ist eng mit der Kosinus-Ähnlichkeit verwandt und eine Schlüsselkomponente im Aufmerksamkeitsmechanismus von Transformern, wo es zur Berechnung der Ähnlichkeit (Scores) zwischen Query- und Key-Vektoren verwendet wird. Es ist ein effizienter Weg, die "Übereinstimmung" von Vektoren zu messen, die in ähnliche Richtungen zeigen. Die Kosinus-Ähnlichkeit ist dabei die robustere Wahl, wenn es darum geht, die reine semantische Bedeutung zu vergleichen, da sie die Vektorlänge normalisiert.
