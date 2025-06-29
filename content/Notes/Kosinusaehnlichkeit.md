---
tags: ["ML", "LLM", "NLP", "Python", "Statistik"]
author: CKe
---

# Kosinusähnlichkeit: Ein Maß für die semantische Ähnlichkeit

Die **Kosinusähnlichkeit** ist eine weit verbreitete Metrik, um die Ähnlichkeit zwischen zwei nicht-null Vektoren in einem inneren Produktraum zu bestimmen. Sie ist besonders populär in der **Verarbeitung natürlicher Sprache (NLP)** und bei **Large Language Models (LLMs)**, da sie hervorragend dazu geeignet ist, die **semantische Ähnlichkeit** von Texten zu messen.

## Was misst die Kosinusähnlichkeit?

Im Grunde misst die Kosinusähnlichkeit den **Kosinus des Winkels zwischen zwei Vektoren**.

* Ein Kosinuswert von **1** bedeutet, dass der Winkel 0 Grad beträgt, d.h., die Vektoren zeigen in exakt dieselbe Richtung. Dies indiziert **maximale Ähnlichkeit**.
* Ein Wert von **0** bedeutet, dass der Winkel 90 Grad beträgt (die Vektoren sind orthogonal). Es gibt **keine Ähnlichkeit** in ihrer Ausrichtung.
* Ein Wert von **-1** bedeutet, dass der Winkel 180 Grad beträgt, d.h., die Vektoren zeigen in exakt entgegengesetzte Richtungen. Dies indiziert **maximale Unähnlichkeit**.

Wichtig ist, dass die Kosinusähnlichkeit **unabhängig von der Größe (Länge)** der Vektoren ist. Sie betrachtet ausschließlich ihre **Ausrichtung im Vektorraum**. Das ist entscheidend, da in vielen Anwendungen (wie Text-Embeddings) die Länge eines Vektors nicht unbedingt eine Rolle für die semantische Bedeutung spielt, sondern nur seine Richtung. Und darin unterscheidet es sich vom [[Skalarprodukt|Skalarprodukt]].


## Formel der Kosinusähnlichkeit

Die Kosinusähnlichkeit zweier Vektoren $\vec{A}$ und $\vec{B}$ wird berechnet als:

$$
\text{Kosinusähnlichkeit}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \cdot ||\vec{B}||}
$$

Dabei ist:
* $\vec{A} \cdot \vec{B}$ das **Skalarprodukt (Dotprodukt)** der Vektoren $\vec{A}$ und $\vec{B}$.
* $||\vec{A}||$ die **euklidische Norm (Länge)** des Vektors $\vec{A}$.
* $||\vec{B}||$ die **euklidische Norm (Länge)** des Vektors $\vec{B}$.

---

## Anwendungsbereiche in LLMs und NLP

Die Kosinusähnlichkeit ist eine Schlüsselkomponente in modernen NLP-Systemen:

* **Semantische Suche und [[RAG|Retrieval Augmented Generation (RAG)]]:** Wenn man eine Frage an ein LLM stellt, wird die Frage in einen Vektor (Embedding) umgewandelt. Dieses Embedding wird dann mit den Embeddings einer Wissensdatenbank (häufig [[Vektordatenbank|Vektordatenbanken]]) verglichen, um die relevantesten Dokumente oder Passagen zu finden. Die Kosinusähnlichkeit hilft dabei, die "nächsten" oder semantisch ähnlichsten Inhalte zu identifizieren.
* **Empfehlungssysteme:** Produkte, Filme oder Artikel, die ähnliche inhaltliche Beschreibungen oder Nutzerprofile aufweisen, können anhand der Kosinusähnlichkeit ihrer Embeddings empfohlen werden.
* **Text-Clustering und Klassifizierung:** Texte mit hoher Kosinusähnlichkeit werden zu Gruppen (Clustern) zusammengefasst oder bestimmten Kategorien zugeordnet, da sie wahrscheinlich ein ähnliches Thema behandeln.
* **Plagiatserkennung:** Durch den Vergleich der Kosinusähnlichkeit von Textsegmenten kann die Ähnlichkeit gemessen und mögliche Plagiate identifiziert werden.

Die Fähigkeit der Kosinusähnlichkeit, die "Bedeutung" oder "Thematik" von Texten durch die Vektorausrichtung zu erfassen, macht sie zu einem unverzichtbaren Werkzeug im Zeitalter der KI und des maschinellen Lernens.
