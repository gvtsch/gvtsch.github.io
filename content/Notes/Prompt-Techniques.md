---
title: Prompt-Strategien
tags: ["python", "ml", "llm", "nlp"]
author: CKe
---

# Prompt-Strategien und -Techniken

Im Bereich der Large Language Models (LLMs) gibt es verschiedene etablierte Techniken und Muster für die Gestaltung von Prompts, die die Qualität und Präzision der Antworten des Modells maßgeblich beeinflussen können. Ein paar habe ich hier gelistet.

## Zero-Shot Prompting

* **Beschreibung:** Die grundlegendste Form. Die Aufgabe oder Frage wird dem LLM direkt gestellt, ohne vorherige Beispiele. Das Modell muss die Aufgabe allein auf Basis des Wissens, mit dem es trainiert wurde, lösen.
* **Beispiel:** `"Klassifiziere den folgenden Satz als positiv oder negativ: 'Der Service war ausgezeichnet.' "`

## Single-Shot Prompting

* **Beschreibung:** Dem LLM wird ein einziges Beispiel gegeben, das zeigt, wie die Antwort strukturiert oder formatiert sein soll, bevor die eigentliche Aufgabe gestellt wird.
* **Beispiel:** `"Frage: Hauptstadt von Frankreich? Antwort: Paris. Frage: Höchster Berg der Erde? Antwort:"`

## Few-Shot Prompting

* **Beschreibung:** Eine Erweiterung des Single-Shot Promptings, bei der dem LLM mehrere Beispiele für Aufgaben und deren korrekte Lösungen präsentiert werden. Dies hilft dem Modell, komplexere Muster, Beziehungen oder spezifische Formate besser zu erkennen.
* **Beispiel:**
    * `"Frage: Das Auto ist rot. Negativ: Das Auto ist nicht rot.`
    * `Frage: Ich bin glücklich. Negativ: Ich bin nicht glücklich.`
    * `Frage: Der Himmel ist blau. Negativ:"`

## Chain-of-Thought (CoT) Prompting

* **Beschreibung:** Das LLM wird explizit aufgefordert, seine Schritte zur Problemlösung oder seine Überlegungen aufzuschreiben, bevor es die finale Antwort gibt. Dies verbessert die Genauigkeit bei komplexen Aufgaben und erhöht die Transparenz.
* **Beispiel:** `"Erkläre Schritt für Schritt, wie man einen Kuchen backt."` oder `"Löse die folgende Aufgabe und zeige alle Rechenschritte: ..." `
* _Das kann man beliebig komplex gestalten, siehe zum Beispiel [[ReAct|2025-07-14-ReAct]]_

## Tree-of-Thought (ToT) Prompting

* **Beschreibung:** Eine fortgeschrittenere Variante von CoT. Das LLM wird angeleitet, nicht nur eine lineare Gedankenkette zu verfolgen, sondern mehrere mögliche Wege oder Zwischenschritte zu erkunden, diese zu bewerten und gegebenenfalls schlechte Pfade zu verwerfen, um den besten Lösungsweg zu finden.
* **Beispiel:** `"Aufgabe: Entwickle eine Strategie, um die monatlichen Stromkosten in einem kleinen Haushalt signifikant zu senken. Gehe dabei wie folgt vor: 1.  Schlage mindestens drei unterschiedliche Ansätze vor. 2.  Bewerte für jeden Ansatz kurz die potenziellen Vor- und Nachteile (Effizienz, Kosten, Aufwand). 3.  Empfiehl basierend auf deiner Bewertung den vielversprechendsten Ansatz und begründe deine Wahl." `

## Persona Pattern

* **Beschreibung:** Dem LLM wird eine spezifische Rolle oder Persönlichkeit zugewiesen. Dies beeinflusst den Ton, den Stil, die Wortwahl und die Art und Weise, wie das Modell Informationen verarbeitet oder präsentiert, um konsistente und kontextuell passende Antworten zu erhalten.
* **Beispiel:** `"Verhalte dich wie ein erfahrener Wissenschaftler und erkläre das Konzept der Relativitätstheorie."`

## Interview Pattern

* **Beschreibung:** Die Interaktion mit dem LLM wird als Interview strukturiert, bei dem man Fragen stellt und das LLM in der Rolle des Befragten antwortet. Das ist nützlich, um gezielt Informationen abzufragen oder eine simulierte Gesprächssituation zu erzeugen. Die Rollen können dabei flexibel getauscht werden.
* **Beispiel**:
    * **Nutzer als Interviewer**: `"Ich bin der Interviewer. Du bist der Kandidat für die Position als Softwareentwickler. Frage 1: Erzähle mir von deinen Erfahrungen mit Python."` 
    * **LLM als Interviewer**: Man könnte dem LLM die Anweisung geben: `"Ich bin ein Experte für künstliche Intelligenz. Stelle mir drei Fragen zu den Herausforderungen von LLMs."`
    * **Interaktion zwischen zwei LLMs (simuliert)**: In komplexeren Agentensystemen könnte man sogar zwei unterschiedliche LLM-Agenten so prompten, dass sie ein Interview miteinander führen, beispielsweise um ein Problem aus verschiedenen Perspektiven zu beleuchten oder Wissen auszutauschen, z.B. zwei unterschiedliche Persona Patterns.

## Self-Consistency Prompting

* **Beschreibung:** Das LLM wird aufgefordert, eine Aufgabe mehrmals zu lösen, wobei es jedes Mal einen unabhängigen Gedankengang verfolgt. Die verschiedenen generierten Antworten werden verglichen, und die am häufigsten vorkommende oder konsistenteste Antwort wird als finale Lösung gewählt, was die Robustheit und Genauigkeit erhöht.
* **Beispiel:** `"Aufgabe: Wenn du einen Sack Äpfel hast und drei Viertel davon rot sind, der Rest grün, wie viele Äpfel sind dann grün, wenn der Sack 16 Äpfel enthält? Bitte löse diese Aufgabe dreimal. Zeige für jeden Versuch deine Schritte. Gib abschließend die Antwort an, die in deinen Versuchen am häufigsten vorkommt."`

## Generated Knowledge Prompting

* **Beschreibung:** In einem ersten Schritt generiert das LLM selbst relevantes Wissen oder Fakten zum Thema. In einem zweiten Schritt verwendet es dieses selbst generierte Wissen als Kontext, um die ursprüngliche Frage zu beantworten, was die Antwortqualität verbessern kann.
* **Beispiel:** `"Schritt 1: Generiere drei Fakten über die Photosynthese. Schritt 2: Erkläre anhand dieser Fakten, warum Pflanzen Sonnenlicht benötigen."`

## Constraint-Based Prompting

* **Beschreibung:** Man definiert explizite Regeln, Einschränkungen oder Formate, die die Ausgabe des LLM einhalten muss. Das ist wichtig, wenn eine strukturierte oder spezifisch formatierte Antwort benötigt wird.
* **Beispiel:** `"Fasse den Text in maximal 50 Wörtern zusammen."`, `"Gib die Antwort als JSON-Objekt mit den Feldern 'Name' und 'Alter' zurück."`

## Iterative Prompting / Prompt Refinement

* **Beschreibung:** Diese Technik ist eher ein Workflow. Man beginnt mit einem groben Prompt, analysiert die Antwort des LLM und verfeinert dann das Prompt schrittweise basierend auf dem Ergebnis oder Feedback, um die Antwortqualität zu verbessern.
* **Beispiel:** Zuerst: `"Schreibe einen Marketingtext für ein neues Smartphone."` Dann: `"Gut, aber mach ihn kürzer und erwähne die Akkulaufzeit explizit."`

Diese Liste ist alles andere als vollständig, aber es handelt sich um Techniken, die jeder schnell in seinen Alltag einbinden kann, ohne sich z.B. mit neuen Tools vertraut machen zu müssen.