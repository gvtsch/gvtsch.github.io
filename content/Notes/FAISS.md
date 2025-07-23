---
tags: ["faiss", "vektordatenbank", "llm", "rag", "ml", "nlp", "python", "statistik"]
author: CKe
date: 2025-07-14
---

# `FAISS` - Facebook AI Similarity Search

`FAISS` ist eine Bibliothek, die von Facebook AI Research (also von Meta) entwickelt wurde, um effiziente Ähnlichkeitssuchen (z.B. [[Kosinusaehnlichkeit]], [[Skalarprodukt]]) durchzuführen. `FAISS` ist hinsichtlich künstlicher Intelligenz und insbesondere für Large Language Models (LLMs) ein sehr wichtiges Werkzeug, da es (wie auch andere Tools wie z.B. Pinecone) die Grundlage für Retrieval Augmented Generation ([[RAG]]) bildet.

## Was macht `FAISS` so wichtig?

LLMs sind bekanntermaßen in ihrem Wissen auf ihre Trainingsdaten beschränkt. Um spezifisches, aktuelles oder proprietäres Wissen (quasi das Gegenteil zu Open-Source-Wissen) zugänglich zu machen, werden RAG-Systeme genutzt. An der Stelle kommt `FAISS` ins Spiel:

1. **Vektor-Embedding**: Texte (ganze Dokumente, einzelne Absätze, Sätze, ...) werden von Embedding-Modellen in numerische Vektoren umgewandelt. Diese Vektoren repräsentieren die semantische Bedeutung des Texts. Ähnliche Texte haben ähnliche Vektoren und liegen im viel-dimensionalem Vektorraum nah beienander.
2. **Effiziente Suche**: Wenn ein Nuzter eine Frage stellt, wird diese Frage ebenfalls vektorisiert. `FAISS` ermöglicht dann, mit Ähnlichkeitssuchen sehr schnell die ähnlichsten Dokumentvektoren in dieser ggf. riesigen Datenbank zu finden. `FAISS` verwendet dafür optimierte Algorithmen und Datenstrukturen, um diese Suchen effizient zu gestalten.
3. **Skalierbarkeit**: `FAISS` ist darauf ausgelegt Milliarden von Vektoren zu behandeln. Das wird spätestens bei großen Datenbanken entsprechend wichtig, weil schließlich große Korpora von Dokumenten indizert werden müssen.
4. **Hardware-Optimierung**: Man kann GPUs einsetzen um die Suchvorgänge weiter zu beschleunigen.

Ohne einer effizienten Vektordatenbank wäre die Suche in großen Datensätzen viel zu langsam, um Echtzeit-RAG-Anwendungen zu ermöglichen.

## Wie funktioniert `FAISS` nun?

Das ganze werde ich nun stark vereinfachen. Stell dir vor, du hast Millionen von Fotos und möchtest schnell alle finden, die einem bestimmten Referenzfoto ähneln. Du könntest natürlich jedes Foto einzeln visuell vergleichen. Das dürfte ggf. etwas länger dauern. Ähnlich sieht es eben auch bei Texten und ihren Vektoren aus. `FAISS` geht dann in etwa so vor:

1. **Indizierung**: `FAISS` verwendet verschiedene Indextypen, um die Vektoren zu organisieren. Diese Indizes sind optimiert, um die Ähnlichkeistssuche zu beschleunigen.
   * **Flat Index**: Speichert Vektoren direkt und führt eine Brute-Force-Suche durch. Genauer aber langsam bei großen Datenmengen.
   * **Inverted File Index**: Clustern der Vektoren, um die Suche auf relevante Cluster zu beschränken. Schneller, aber mit geringem Genauigkeitsverlust.
   * **Product Quantization**: Komprimiert Vektoren, um den Speicherbedarf zu reduzieren und die Suche zu beschleunigen. Führt ebenfalls zu Genauigkeitsverlusten.
2. **Suche**: Wenn die Abfrage, also der Vektor der Nutzerfrage, kommt, nutzt `FAISS` den gewählten Index, um die `k`-ähnlichsten Vektoren im Datensatz zu finden. Die "Ähnlichkeit" wird dabei oft über die [[Kosinusaehnlichkeit]] gemessen.

Natürlich hängt die Wahl des Indizes nun von den Anforderungen an Geschwindigkeit, Genauigkeit und Speichernutzung ab.

## `FAISS` in [[LangChain]]

In `LangChain` wird es als eine unterstützende Vektordatenbank (oder Vectorstore) integriert. Nachdem die Dokumente geladen und in Chunks geteilt wurden, werden diese Chunks in Vektoren umgewandelt (z.B. mit `OpenAIEmbeddings`). Diese Vektoren werden dann an `FAISS` übergeben, um sie zu indizieren.

Ich möchte das mal an einem Beispiel verdeutlichen.

```python
import os
from dotenv import load_dotenv # Importiere load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory

# API-Key laden
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API-Schlüssel nicht gefunden. Bitte setze ihn in deiner .env-Datei oder als Umgebungsvariable.")

# OpenAI Schnittstelle vorbereiten
llm = OpenAI(temperature=0, api_key=api_key)

# Embedding Model initialisieren
embeddings = OpenAIEmbeddings(api_key=api_key)

# Erzeugen einer PDF falls nicht vorhanden mit Dummy Text
pdf_path = "example_attention.pdf"
if not os.path.exists(pdf_path):
    print(f"Erstelle Dummy-PDF: {pdf_path}")
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, "Attention Is All You Need")
    c.drawString(100, 730, "Autoren: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit,")
    c.drawString(100, 710, "Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin.")
    c.drawString(100, 690, "Attention ist ein Mechanismus in neuronalen Netzen, der es dem Modell ermöglicht,")
    c.drawString(100, 670, "sich auf relevante Teile der Eingabe zu konzentrieren. Es ist eine Funktion,")
    c.drawString(100, 650, "die eine Anfrage und eine Reihe von Schlüssel-Wert-Paaren auf einen Ausgang abbildet.")
    c.drawString(100, 630, "Der Transformer nutzt Attention als Kernkomponente und verzichtet komplett auf Rekurrenz.")
    c.save()
else:
    print(f"Verwende vorhandene PDF-Datei: {pdf_path}")

# Laden der PDF
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Initialisieren des Text-Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs) # Teile die Dokumente in Chunks auf

print(f"Anzahl der erstellten Text-Chunks: {len(splits)}")

# Embeddings erzeugen und Vektordatenbank (FAISS) erstellen
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
print("FAISS Vektordatenbank erfolgreich erstellt.")

# Konversationsspeicher (Memory) initialisieren
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True)

# 7. ConversationalRetrievalChain erstellen
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(), # Macht den FAISS-Vektorspeicher "abrufbar"
    memory=memory
)

# --- 8. Interaktion mit dem Chatbot ---
print("\n--- Starte Chat-Interaktion ---")

user_question1 = "Was ist Attention?"
print(f"User: {user_question1}")
response1 = conversation_chain.invoke({"question": user_question1})
print("Bot:", response1['answer'])

user_question2 = "Wer ist der Autor?"
print(f"\nUser: {user_question2}")
response2 = conversation_chain.invoke({"question": user_question2})
print("Bot:", response2['answer'])

print("\n--- Chat-Interaktion beendet ---")
```

### Wie der Code die [[RAG]]-Pipeline umsetzt
Das Code-Beispiel demonstriert die grundlegenden Schritte einer RAG-Pipeline in [[LangChain]] und die zentrale Rolle von `FAISS`:
1. **Laden und Teilen**: `PyPDFFoader` und `RecursiveCharacterTextSplitter` laden das Dokument und teilen es in verwaltbare Text-Chunks auf.
2. **Vektorisierung**: `OpenAIEmbeddings` wandelt dies Text-Chunks in in Vektoren bzw. [[Embeddings]] um.
3. **Indizierung (`FAISS`)**: `FAISS.from_document` indiziert die Vektoren. Hier organisiert `FAISS` die Datenbank, um die spätere Suche zu beschleunigen.
4. **Abruf und Generierung**: `ConversationalRetrievalChain` verwendet  `vectorstore.as_retriever()`, um bei einer Nutzeranfrage (z.B. _"Was ist Attention?"_) die ähnlichsten Vektoren (also die relevantesten Text-Chunks) aus `FAISS` abzurufen und diese dem LLM zur Generierung der Antwort bereitzustellen.

### Persistenz des `FAISS`-Index: Speichern und Laden
Im obigen Beispiel wird der `FAISS`-Index im Arbeitsspeicher erstellt. Für praktische Anwendungen ist es wichtig, den Index zu speichern, um die zeitaufwändige Vektorisierung der Dokumente bei jeder Ausführung zu vermeiden. Das lässt sich im Grunde sehr einfach lösen.

Speichern:
```python
vectorstore.save_local("faiss_index_directory")
```

Laden:
```python
# Wichtig: Das Embedding-Modell muss beim Laden übergeben werden
loaded_vectorstore = FAISS.load_local("faiss_index_directory", embeddings)
```

### Ausgabe des Beispiels
```
Erstelle Dummy-PDF: example_attention.pdf
Anzahl der erstellten Text-Chunks: 1
FAISS Vektordatenbank erfolgreich erstellt.

--- Starte Chat-Interaktion ---
User: Was ist Attention?
Bot:  Attention ist ein Mechanismus in neuronalen Netzen, der es dem Modell ermöglicht, sich auf relevante Teile der Eingabe zu konzentrieren. Es ist eine Funktion, die eine Anfrage und eine Reihe von Schlüssel-Wert-Paaren auf einen Ausgang abbildet.

User: Wer ist der Autor?
Bot:  Die Autoren von Attention sind Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, ■ukasz Kaiser und Illia Polosukhin.

User: Erinnerst du dich, worüber wir zuerst gesprochen haben?
Bot:  Attention ist ein Mechanismus in neuronalen Netzen, der es dem Modell ermöglicht, sich auf relevante Teile der Eingabe zu konzentrieren. Es ist eine Funktion, die eine Anfrage und eine Reihe von Schlüssel-Wert-Paaren auf einen Ausgang abbildet.

--- Chat-Interaktion beendet ---
```

Der Ausgabe kann man entnehmen, dass zum einen eine Dummy-PDF-Datei erzeugt wurde, und zum anderen, dass in genau dieser Datei die Informationen gesucht und auch gefunden werden. 

## Zusammanfassung

`FAISS` ist also ein entscheidender Baustein in modernen LLM-Anwendungen. Es ermöglicht, dass LLMs schnell und präzise auf eine ständig wachsende Menge an spezifischen Informationen zugreifen können, um z.B. auch aktuelles oder proprietäres Wissen verarbeiten zu können.
