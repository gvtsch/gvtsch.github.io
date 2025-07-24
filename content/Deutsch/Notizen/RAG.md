---
tags: ["ml", "llm", "nlp", "python", "statistik", "vektordatenbank", "rag"]
author: CKe
title: 'RAG'
---

# Retrieval Augmented Generation

## Was ist RAG?

RAG, oder Retrieval-Augmented Generation, ist ein entscheidender Ansatz im Bereich der Verarbeitung natürlicher Sprache (NLP). Es handelt sich um eine Technik, die Large Language Models (LLMs) wie ChatGPT oder Gemini befähigt, auf Informationen zuzugreifen, die nicht in ihren ursprünglichen Trainingsdaten enthalten sind.

Der Hauptgrund für die Entwicklung von RAG liegt darin, die Schwächen traditioneller LLMs zu überwinden. Diese Modelle neigen oft dazu, zu „halluzinieren“ (d.h., faktisch falsche oder erfundene Antworten zu geben) oder sind durch die Daten begrenzt, mit denen sie trainiert wurden. RAG löst dieses Problem, indem es den LLMs ermöglicht, auf eine aktuelle und verifizierbare externe Wissensbasis zuzugreifen.

# Wie funktioniert RAG?

RAG arbeitet in zwei grundlegenden Phasen:
1. **Retrieval (Abruf von Informationen)**: Wenn Sie eine Frage stellen, sucht das RAG-System zuerst in einer externen Wissensdatenbank nach den relevantesten Informationen. Diese Wissensbasis kann alles sein, von einer Sammlung von Dokumenten über aktuelle Nachrichten bis hin zu firmenspezifischen Daten, die in einer sogenannten Vektordatenbank gespeichert sind. Das System identifiziert die relevantesten „Schnipsel“ oder Dokumente, die zur Beantwortung Ihrer Frage nützlich sind.
2. **Augmentation und Generierung**: Im zweiten Schritt werden diese abgerufenen Informationen der ursprünglichen Benutzeranfrage hinzugefügt. Das LLM erhält nun einen angereicherten Kontext, der alle notwendigen Fakten enthält. Das Modell nutzt diesen „augmentierten“ Prompt, um eine präzise und fundierte Antwort zu generieren.

## Die Vorteile von RAG

Das Ergebnis von RAG ist eine KI-Antwort, die nicht nur flüssig und kohärent ist, sondern vor allem faktisch korrekt und aktuell. Indem das Modell auf überprüfbare Quellen zugreift, wird die Gefahr von Halluzinationen minimiert und die Vertrauenswürdigkeit des Systems erheblich gesteigert. RAG macht LLMs zu zuverlässigen Werkzeugen für spezifische, wissensbasierte Aufgaben und auch um z.B. seine eigenen Dateien zu durchsuchen (an der Stelle würde ich aber davon abraten, OpenAI, Gemini usw. mit diesen Informationen zu versorgen.)