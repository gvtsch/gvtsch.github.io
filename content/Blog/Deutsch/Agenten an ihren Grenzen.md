---
title: Agenten an ihren Grenzen
tags:
    - langchain
    - langgraph
    - python
    - machine-learning
---

# Agenten an ihren Grenzen

## Die Grenzen der LangChain-Kette

In [[ReAct]] haben wir über einen Agenten mit vielen Möglichkeiten geredet und diesen auch programmiert und eingesetzt. ReAct-Agenten sind großartig für kleinere Workflows oder Tool-Aufrufe und auch für Prototypen geeignet.

Doch stoßen ReAct-Agenten bei komplexeren Aufgaben schnell an ihre Grenzen. Ihre Architektur ist primär eine lineare Kette mit einer einfachen und begrenzten Schleife. Sobald Aufgaben wie Selbstkorrektur, Kollaboration zwischen mehreren Agenten oder komplexe Entscheidungslogik gefragt sind, reicht diese Struktur nicht mehr aus.

Um diese Herausforderungen zu meistern, lohnt sich der Wechsel zu einer sogenannten Graphen-Struktur.

---

## Beispiel: Ein ReAct-Agent stößt an seine Grenzen

Stellen wir uns vor, wir möchten einen Agenten bauen, der Python-Code testen, bei Fehlern selbstständig korrigieren und je nach Ergebnis entweder eine Analyse durchführen oder an einen Menschen eskalieren soll. Mit einem klassischen ReAct-Agenten in LangChain ist das nicht möglich – die Grenzen werden schnell sichtbar.

**LangChain ReAct-Agent (klassisch):**
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

def test_code(code: str) -> str:
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return "Success"
    except Exception as e:
        return f"Error: {e}"

def analyze_output(output: str) -> str:
    return f"Analysis: {output}"

def escalate_to_human(output: str) -> str:
    return f"Escalated to human: {output}"

tools = [
    Tool(name="CodeTester", func=test_code, description="Tests Python code."),
    Tool(name="Analyzer", func=analyze_output, description="Analyzes output."),
    Tool(name="Escalator", func=escalate_to_human, description="Escalates to human.")
]

llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

# The agent tries once, cannot retry, cannot branch in code, no shared state
result = agent.run("Test this code and analyze the output or escalate if there is an error:\nprint(x)")
print(result)
```

**Was passiert hier?**

- Der Agent ruft das Tool auf und erhält einen Fehler (`NameError: name 'x' is not defined`).
- Er kann aber **nicht** automatisch einen weiteren Versuch starten oder den Fehler gezielt beheben (keine Schleife/Selbstkorrektur).
- Die Entscheidung, ob analysiert oder eskaliert wird, ist im Prompt versteckt und nicht im Code abbildbar (kein explizites Branching).
- Es gibt keinen gemeinsamen Status, den mehrere Agenten oder Tools teilen könnten (kein Shared State).

**Visualisierung:**  
```
[User prompt] 
     |
     v
[Agent: Test code]
     |
     v
[Tool: Error detected]
     |
     v
[Agent: No further action]
```

**Fazit:**  
Dieses Beispiel macht deutlich, dass klassische ReAct-Agenten bei komplexeren Aufgaben schnell an ihre Grenzen stoßen. Sie können nicht iterativ Fehler beheben, nicht flexibel verzweigen und keinen gemeinsamen Status verwalten.  
Eine graphbasierte Architektur wie LangGraph löst genau diese Probleme – dazu mehr im nächsten Abschnitt.

---

## Drei zentrale Grenzen klassischer Agenten

### 1. Fehlende explizite Schleifensteuerung und Selbstkorrektur

Klassische Agenten-Frameworks wie LangChain bieten keine echte, programmatische Iteration oder Selbstkorrektur. Der Agent kann Fehler nicht autonom beheben oder Ergebnisse gezielt verfeinern. Die Standard-Agenten-Schleife ist darauf ausgelegt, möglichst schnell zu einer finalen Antwort zu gelangen – interne Iterationen sind nicht vorgesehen.

Wenn beispielsweise ein Tool-Aufruf fehlschlägt (etwa ein Code-Test einen Fehler liefert), gibt es keine klare Anweisung im Code, den Fehlerbehebungs-Zyklus zu wiederholen. Die gesamte Verantwortung für Korrekturen liegt beim LLM und ist im Prompt versteckt – das ist fehleranfällig und schwer nachvollziehbar. Auch das Debugging gestaltet sich schwierig, da die Schleifen- und Korrekturlogik nicht explizit im Code, sondern im Prompt verborgen ist.

---

### 2. Komplexes Branching und Blackbox-Logik

Ein weiteres Problem klassischer LangChain-Ketten ist das Handling von komplexen Verzweigungen. Oft muss sich der Workflow je nach Ergebnis eines Zwischenschritts unterschiedlich verhalten. In LangChain muss die gesamte Verzweigungslogik jedoch im Prompt formuliert werden („Wenn Ergebnis X, dann Tool A, sonst Tool B“). Das macht die Logik schwer wartbar, fehleranfällig und unflexibel – eine kleine Änderung im Prompt kann den gesamten Workflow beeinflussen.

Es fehlt ein klarer Mechanismus im Code, um den nächsten Schritt basierend auf einem Zwischenstand zu definieren. Die Steuerung liegt im LLM (Blackbox) und nicht im Code (Graph). Mit wachsender Komplexität werden solche Ketten schnell unübersichtlich und schwer zu pflegen. Graphenstrukturen hingegen sind modular, leichter zu erweitern und erlauben explizites Branching.

**Typische Szenarien:** Human-in-the-Loop, Eskalationspfade oder die Auswahl zwischen verschiedenen Spezial-Tools lassen sich mit klassischen Ketten kaum sauber abbilden.

---

### 3. State Management und Multi-Agenten-Kollaboration

Gerade bei Projekten, in denen mehrere Agenten zusammenarbeiten, stößt die klassische Kette an ihre Grenzen. LangChain ist primär zustandslos – für Langzeitprojekte oder kollaborative Szenarien ist das unzureichend. Es gibt keine native, saubere Möglichkeit, die Kontrolle dynamisch zwischen spezialisierten Agenten (z.B. Recherche-Agent ↔ Analyse-Agent) zu übergeben.

Agenten benötigen oft einen gemeinsamen, veränderbaren Projektstatus (Shared State), auf den alle zugreifen und den sie aktualisieren können, bevor die Kontrolle weitergegeben wird. Die lineare Kette bietet hierfür keinen nativen Mechanismus. Zudem lassen sich in Graph-Workflows einzelne Knoten gezielt parallelisieren oder optimieren – das ist mit linearen Ketten nicht möglich.

---

### Weitere Herausforderungen

- **Integration von Human-in-the-Loop:** Mit Graphen kann man explizit menschliche Eingriffe (z.B. Review-Schritte) einbauen.
- **Transparenz und Debugging:** In klassischen LangChain-Ketten ist es oft schwer, den genauen Ablauf und Fehlerquellen nachzuvollziehen, weil viel Logik im Prompt und nicht im Code steckt. Mit LangGraph ist der Ablauf explizit im Code sichtbar und besser testbar.

## Fazit: Die Lösung ist der Graph

Um die genannten Probleme zu lösen, braucht es eine Architektur, die nicht-linear, zustandsbehaftet und explizit steuerbar ist. Genau das bietet **LangGraph** – eine Erweiterung von LangChain, die auf Graphen basiert.

Mit LangGraph lassen sich Knoten (Nodes) und Kanten (Edges) explizit definieren. Das ermöglicht native Loops, sauberes Branching, parallele Ausführung und eine gemeinsame State-Verwaltung. Der Übergang zur Graphen-Struktur ist entscheidend, um Agenten produktionsreif, zuverlässig und komplex zu machen.

**Neugierig geworden?** Dann probiere LangGraph aus und bringe deine Agenten-Workflows auf das nächste Level!