---
tags: ["langchain", "langgraph", "ml", "llm", "nlp"]
author: CKe
---

# Einführung in LangGraph

LangGraph mag auf den ersten Blick komplex wirken, aber seine Kernideen sind sehr intuitiv.


## Was ist LangGraph?

Stellen dir **LangGraph** als ein leistungsstarkes Werkzeug vor, um **KI-Agenten** oder **Chatbots** zu entwickeln, die über einfache, lineare Abläufe hinausgehen. Im Gegensatz zu herkömmlichen LangChain-Ketten, die meist einen festen Schritt-für-Schritt-Prozess (A -> B -> C) definieren, ermöglicht LangGraph:

* **Entscheidungsfindung:** Agenten können basierend auf dem aktuellen Zustand oder bestimmten Kriterien entscheiden, welchen nächsten Schritt sie ausführen.
* **Schleifen und Iterationen:** Es ist möglich, dass ein Agent bestimmte Schritte wiederholt, bis eine Bedingung erfüllt ist (z.B. solange noch offene Fragen existieren).
* **Zustandsverwaltung (Shared Memory):** Alle beteiligten Agenten oder Schritte teilen sich einen zentralen "Gedächtnisbereich" (den Zustand), der über den gesamten Workflow hinweg aktualisiert wird.

Kurz gesagt: LangGraph erweitert [[LangChain]] um die Fähigkeit, **komplexe, zustandsbehaftete und zyklische Multi-Agenten-Workflows** zu erstellen. 

## Das Beispiel
Ich möchte versuchen das alles an einem Beispiel zu erarbeiten. In dem Beispiel soll ein Agenten-Netzwerk eine Anforderung analysieren und ggf. in Datenbanken nach Antworten auf offene Fragen suchen. Wenn die Fragen beantwortet sind oder nicht weiter geklärt werden können, soll es zum Abschluss kommen.

## Die Kernkonzepte von LangGraph

Zunächst mal geht es um vier Zentrale Bausteine, um LangGraph besser zu verstehen.

### 1. **Graph (Der Workflow)**
Das ist das übergeordnete Modell des gesamten Agentensystems. Ein Graph ist eine Sammlung von **Knoten** und **Kanten**, die definieren, wie der Agenten-Workflow aufgebaut ist und abläuft. Er repräsentiert die gesamte Logik des Systems.

### 2. **Node (Knoten)**
Ein Knoten ist ein **einzelner, atomarer Schritt** oder eine Aktion innerhalb des Workflows. Jeder Knoten ist im Wesentlichen eine Python-Funktion, die den aktuellen Zustand erhält, eine Aufgabe ausführt und den aktualisierten Zustand zurückgibt.

In einem Framework könnten die Knoten beispielsweise sein:
* Ein **`ExpertCollaborationNode`**, der die initialen Anforderungen analysiert und erste Fragen generiert.
* Ein **`DataExpertQueryNode`**, der ein Multi-Agent-RAG-Framework aufruft, um Fragen zu beantworten.
* Ein **`FollowUpAnalysisNode`**, der weitere Analysen durchführt und dabei potenziell neue Fragen entdeckt.
* Ein **`DecisionNode`**, der prüft, ob der Workflow fortgesetzt oder beendet werden soll.

### 3. **Edge (Kante)**
Eine Kante definiert den **Übergang von einem Knoten zum nächsten**. Sie zeigt an, in welcher Reihenfolge die Schritte im Graphen ausgeführt werden sollen.

Es gibt zwei Haupttypen von Kanten:
* **Standard-Kanten (`add_edge`):** Diese Kanten sind direkt und sagen: "Nach Knoten A gehe immer zu Knoten B." Sie definieren einen festen Pfad.
* **Konditionale Kanten (`add_conditional_edges`):** Das ist der Schlüssel für dynamische und iterative Workflows! Eine konditionale Kante sagt: "Nach Knoten A, rufe eine separate **Entscheidungsfunktion** auf. Basierend auf dem Rückgabewert dieser Funktion gehe entweder zu Knoten B, C oder D." Hier würde man die Logik implementieren, die entscheidet, ob man zum Datenexperten zurückkehrt oder die Analyse abschließen.

### 4. **State (Zustand)**
Der Zustand ist das **gemeinsame "Gedächtnis"** des Graphen. Er ist ein Python-Objekt (oft ein `TypedDict`), das alle relevanten Informationen enthält, die der Workflow benötigt und die von den Knoten aktualisiert werden.

Beispiele für Elemente im Zustand/State:
* `requirements_doc`: Das sich entwickelnde Anforderungsdokument.
* `open_questions`: Eine Liste von Fragen, die noch beantwortet werden müssen.
* `answered_questions`: Ein Dictionary, das bereits beantwortete Fragen und ihre Antworten speichert.
* `new_questions_arisen`: Neue Fragen, die während späterer Analyseschritte aufgetaucht sind.
* `current_analysis_context`: Der aktuelle Kontext oder Fokus der Analyse.

Jeder Knoten erhält den aktuellen Zustand als Input, führt seine Operation aus und gibt den möglicherweise aktualisierten Zustand zurück. So können Informationen nahtlos durch den gesamten Workflow fließen und von allen beteiligten Komponenten genutzt werden.

---

## Ihr erster LangGraph-Workflow: Ein "Hello World" Beispiel

Lassen Sie uns die Theorie mit einem einfachen, aber funktionsfähigen Beispiel illustrieren, das die Kernkonzepte Ihres Anwendungsfalls (Fragen stellen, Antworten erhalten, entscheiden, ob neue Fragen nötig sind) abbildet.

```python
from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, END # END ist ein spezieller Marker für das Ende des Graphen

### 1. Zustand definieren (Das gemeinsame Gedächtnis des Workflows)
class AnalysisWorkflowState(TypedDict):
    """
    Definiert den gemeinsamen Zustand, der durch den LangGraph-Workflow fließt.
    """
    initial_requirements: str        # Die ursprünglichen Anforderungsbeschreibung
    open_questions: List[str]      # Aktuelle Liste von Fragen, die an den Datenexperten gehen sollen
    answered_questions: Dict[str, str] # Dictionary {Frage: Antwort} der bereits beantworteten Fragen
    analysis_phase: str            # Aktuelle Phase der Analyse (z.B. "initial", "detailed", "review")
    new_questions_from_analysis: List[str] # Fragen, die während der 'weiteren Schritte' entstehen können
    iteration_count: int           # Zähler für die Schleifendurchläufe (zur Demonstration)

### 2. Knoten definieren (Die logischen Schritte des Workflows)

def generate_initial_questions_node(state: AnalysisWorkflowState) -> AnalysisWorkflowState:
    """
    Knoten, der die anfänglichen Fragen aus den Anforderungen ableitet.
    Dieser Knoten simuliert Ihre "Experten-Zusammenarbeit" (LangChain-Experten).
    """
    print("\n--- Knoten: Initialfragen generieren ---")
    
    # Hier würde Ihre LangChain-Logik für die Experten-Zusammenarbeit greifen.
    # Sie würden die initial_requirements analysieren und erste Fragen formulieren.
    
    initial_q = [
        "Wie viele Benutzer werden das System voraussichtlich gleichzeitig nutzen?",
        "Welche Art von Daten wird gespeichert (personenbezogen, sensibel)?",
        "Gibt es spezielle Compliance-Vorgaben (z.B. DSGVO, HIPAA)?"
    ]
    print(f"Generierte Initialfragen: {initial_q}")
    
    return {
        **state, # Den bestehenden Zustand übernehmen
        "open_questions": initial_q,
        "analysis_phase": "initial_questioning",
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def query_data_expert_node(state: AnalysisWorkflowState) -> AnalysisWorkflowState:
    """
    Knoten, der die offenen Fragen an den Datenexperten (Multi-Agent-RAG) sendet
    und die Antworten integriert.
    """
    print("\n--- Knoten: Datenexperten befragen ---")
    
    questions_to_ask_now = state["open_questions"] + state["new_questions_from_analysis"]
    
    if not questions_to_ask_now:
        print("Keine neuen Fragen für den Datenexperten gefunden.")
        return state # Nichts zu tun
    
    print(f"Fragen an Datenexperten: {questions_to_ask_now}")
    
    current_answered = state.get("answered_questions", {})
    newly_answered = {}
    
    # Hier würde die tatsächliche Interaktion mit Ihrem Multi-Agent-RAG-Framework stattfinden.
    # Für dieses Beispiel simulieren wir die Antworten.
    for q in questions_to_ask_now:
        answer = f"Antwort von Datenexperte auf: '{q}' (Simuliert)"
        newly_answered[q] = answer
        print(f"   -> Beantwortet: '{q}'")
        
    return {
        **state,
        "answered_questions": {**current_answered, **newly_answered}, # Antworten hinzufügen
        "open_questions": [],           # Initialfragen sind jetzt beantwortet
        "new_questions_from_analysis": [], # Neu aufgetretene Fragen sind jetzt beantwortet
        "analysis_phase": "answers_received"
    }

def conduct_follow_up_analysis_node(state: AnalysisWorkflowState) -> AnalysisWorkflowState:
    """
    Knoten für die "weiteren Schritte der Analyse", wo neue Fragen entstehen könnten.
    """
    print("\n--- Knoten: Folgeanalyse durchführen ---")
    
    # In einem echten Szenario würde hier Ihre weitere LangChain-Logik für die Analyse laufen.
    # Basierend auf den bisherigen Anforderungen und Antworten könnten neue Unklarheiten entstehen.
    
    new_questions = []
    # Beispiel-Logik: Nach der ersten Runde könnte eine technische Frage auftauchen
    if state["iteration_count"] == 1 and "Wie viele Benutzer" in state["answered_questions"]:
        new_questions.append("Ist eine mandantenfähige Architektur erforderlich?")
        print(f"Neue Frage während Folgeanalyse entdeckt: '{new_questions[0]}'")
    elif state["iteration_count"] == 2 and "Ist eine mandantenfähige Architektur" in state["answered_questions"]:
        new_questions.append("Welche Technologien sollen für die Datenbank genutzt werden?")
        print(f"Neue Frage während Folgeanalyse entdeckt: '{new_questions[0]}'")
    else:
        print("Keine neuen Fragen während dieser Analysephase entdeckt.")

    return {
        **state,
        "new_questions_from_analysis": new_questions,
        "analysis_phase": "follow_up_analysis",
        "iteration_count": state["iteration_count"] + 1
    }

def decide_workflow_path_node(state: AnalysisWorkflowState) -> str:
    """
    Entscheidungsknoten: Prüft, ob neue Fragen aufgetaucht sind oder der Workflow beendet werden kann.
    """
    print("\n--- Knoten: Workflow-Pfad entscheiden ---")
    
    if state["new_questions_from_analysis"]:
        print("Neue Fragen gefunden! Zurück zum Datenexperten.")
        return "re_query_data_expert"
    elif not state["open_questions"] and not state["new_questions_from_analysis"] and state["iteration_count"] > 2:
        # Beispiel-Abbruchbedingung: Keine offenen Fragen mehr und mindestens 3 Iterationen durchlaufen
        print("Alle Fragen geklärt, Analyse abgeschlossen.")
        return "end_analysis"
    else:
        # Falls es noch unklare Schritte gibt, die weitere Analyse benötigen, aber keine expliziten Fragen
        print("Weiterführende Analysephase benötigt, aber keine direkten Fragen an Datenexperten. Oder noch nicht genug Iterationen.")
        # In einem realen Szenario könnte hier auch "continue_analysis" zurückgegeben werden
        # um zum 'conduct_follow_up_analysis_node' zurückzukehren, ohne den Datenexperten zu befragen.
        # Für dieses Beispiel leiten wir es zum Ende, wenn keine spezifischen neuen Fragen da sind.
        return "end_analysis"


### 3. Graph aufbauen (Verbinden der Knoten mit Kanten)

# 1. Initialisiere den Graphen mit unserem definierten Zustand
workflow = StateGraph(AnalysisWorkflowState)

# 2. Füge die einzelnen Knoten dem Graphen hinzu
workflow.add_node("generate_initial_questions", generate_initial_questions_node)
workflow.add_node("query_data_expert", query_data_expert_node)
workflow.add_node("conduct_follow_up_analysis", conduct_follow_up_analysis_node)

# 3. Setze den Startpunkt des Graphen (wo der Workflow beginnt)
workflow.set_entry_point("generate_initial_questions")

# 4. Definiere die Kanten (Übergänge zwischen den Knoten)

# Nach der Initialfragenerstellung gehen wir IMMER zum Datenexperten
workflow.add_edge("generate_initial_questions", "query_data_expert")

# Nachdem der Datenexperte geantwortet hat, führen wir IMMER die Folgeanalyse durch
workflow.add_edge("query_data_expert", "conduct_follow_up_analysis")

# Nach der Folgeanalyse kommt der Entscheidungsknoten.
# Hier kommt die konditionale Logik ins Spiel:
workflow.add_conditional_edges(
    "conduct_follow_up_analysis", # Der Knoten, von dem aus wir verzweigen
    decide_workflow_path_node,    # Die Funktion, die die Entscheidung trifft
    {
        "re_query_data_expert": "query_data_expert", # Wenn neue Fragen -> zurück zum Datenexperten
        "end_analysis": END                          # Wenn keine neuen Fragen -> Workflow beenden
    }
)

### 4. Graph kompilieren und ausführen

# Der Graph wird "kompiliert" und ist dann bereit zur Ausführung
app = workflow.compile()

# Definieren des initialen Zustands, mit dem der Workflow startet
initial_state = AnalysisWorkflowState(
    initial_requirements="Wir benötigen ein neues System zur Verwaltung von Kundenaufträgen.",
    open_questions=[],
    answered_questions={},
    analysis_phase="start",
    new_questions_from_analysis=[],
    iteration_count=0
)

print("--- Start des LangGraph Workflows zur Anforderungsanalyse ---")
# Starten Sie den Workflow. LangGraph kümmert sich um die Abfolge der Knoten und Schleifen.
final_state = app.invoke(initial_state)

print("\n--- LangGraph Workflow beendet ---")
print("## Finaler Zustand der Analyse:")
print(f"Analysephase: {final_state['analysis_phase']}")
print(f"Gesamtanzahl Iterationen: {final_state['iteration_count']}")
print("--- Alle beantworteten Fragen ---")
for q, a in final_state['answered_questions'].items():
    print(f"- **Frage:** {q}\n  **Antwort:** {a}\n")
