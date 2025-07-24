---
tags: ["ml", "llm", "nlp", "python", "statistik"]
---
# Skalarprodukt (Dotprodukt): Ein Fundament der Vektoralgebra

Das **Skalarprodukt**, auch bekannt als **Dotproduct**, ist eine grundlegende Operation in der linearen Algebra, die zwei Vektoren nimmt und eine einzelne skalare Zahl (daher "Skalarprodukt") zurückgibt. Diese Zahl gibt Aufschluss über die Beziehung der Vektoren zueinander, insbesondere über ihre **relative Ausrichtung** und **Größe**.

## Was misst das Skalarprodukt?

Das Skalarprodukt kann auf zwei Arten interpretiert werden:

1.  **Algebraische Definition:** Es ist die Summe der Produkte der entsprechenden Komponenten zweier Vektoren. Für zwei Vektoren $\vec{A} = (a_1, a_2, \dots, a_n)$ und $\vec{B} = (b_1, b_2, \dots, b_n)$ ist das Skalarprodukt:

    $$
    \vec{A} \cdot \vec{B} = a_1 b_1 + a_2 b_2 + \dots + a_n b_n = \sum_{i=1}^{n} a_i b_i
    $$

2.  **Geometrische Definition:** Es ist das Produkt der Längen (Magnituden) der Vektoren multipliziert mit dem Kosinus des Winkels zwischen ihnen.

    $$
    \vec{A} \cdot \vec{B} = ||\vec{A}|| \cdot ||\vec{B}|| \cdot \cos(\theta)
    $$

    Dabei ist:
    * $||\vec{A}||$ und $||\vec{B}||$ die Längen (Beträge) der Vektoren $\vec{A}$ und $\vec{B}$.
    * $\theta$ der Winkel zwischen den Vektoren $\vec{A}$ und $\vec{B}$.

Diese geometrische Interpretation ist besonders aussagekräftig:
* Wenn $\theta = 0^\circ$ (Vektoren zeigen in dieselbe Richtung), ist $\cos(\theta) = 1$, und das Skalarprodukt ist maximal und positiv.
* Wenn $\theta = 90^\circ$ (Vektoren sind orthogonal), ist $\cos(\theta) = 0$, und das Skalarprodukt ist 0.
* Wenn $\theta = 180^\circ$ (Vektoren zeigen in entgegengesetzte Richtungen), ist $\cos(\theta) = -1$, und das Skalarprodukt ist maximal negativ.

## Zusammenhang zur [[Kosinusaehnlichkeit_de|Kosinusähnlichkeit]]

Das Skalarprodukt ist eng mit der Kosinusähnlichkeit verbunden. Tatsächlich ist die Kosinusähnlichkeit nichts anderes als das **normalisierte Skalarprodukt**. Wenn wir die geometrische Formel nach $\cos(\theta)$ auflösen, erhalten wir genau die Formel für die Kosinusähnlichkeit:

$$
\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \cdot ||\vec{B}||}
$$

Das bedeutet, dass das Skalarprodukt die Kosinusähnlichkeit *inklusive* der Längen der Vektoren liefert. Wenn die Vektoren bereits auf die Länge 1 normalisiert sind (Einheitsvektoren), dann ist das Skalarprodukt direkt gleich der Kosinusähnlichkeit.

## Anwendungsbereiche

Das Skalarprodukt findet breite Anwendung in vielen Bereichen der Wissenschaft und Technik, darunter:

* **Physik:** Berechnung von Arbeit ($W = \vec{F} \cdot \vec{s}$), Leistung oder Fluss von Feldern.
* **Computergraphik:** Bestimmung von Beleuchtungseffekten (z.B. wie hell eine Oberfläche ist, basierend auf dem Winkel zur Lichtquelle) und Kollisionserkennung.
* **Maschinelles Lernen und Neuronale Netze:**
    * **In neuronalen Netzen:** Skalarprodukte (oder Dotproducts) sind die Kernoperation in vielen Schichten, in denen Eingabevektoren mit Gewichtsmatrizen multipliziert werden.
    * **Aufmerksamkeitsmechanismen (z.B. in Transformatoren):** Das Skalarprodukt wird verwendet, um die Ähnlichkeit zwischen "Query"- und "Key"-Vektoren zu berechnen, was bestimmt, wie stark verschiedene Teile der Eingabe miteinander in Beziehung stehen und wie viel "Aufmerksamkeit" sie einander schenken sollen.
    * **Effizienz:** Es ist eine sehr effiziente Operation, die in hochdimensionalen Räumen schnell berechnet werden kann.

Das Skalarprodukt ist also ein wichtiger Baustein, der sowohl theoretische Einblicke in Vektorbeziehungen gibt, als auch die Basis für viele praktische Algorithmen in der modernen Datenverarbeitung und eben auch in Bereichen des Maschinellen-Lernens bildet.
