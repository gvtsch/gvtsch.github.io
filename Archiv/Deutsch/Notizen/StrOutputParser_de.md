---
tags: ["langchain", "llm", "python"]
author: CKe
title: StrOutPutParser
date: 2025-06-29
---

# Was ist `LangChain`'s `StrOutputParser()`?

Der `StringOutputParser()` ist eine Implementierung der [[BaseOutputParser_de|BaseOutputParser]]-Klasse in `LangChain`. Die Hauptfunktion des Parsers ist es, die Ausgabe, die ihm übergeben wird, als einfach String zurückzugeben. Was im ersten Moment trivial klingt, ist entscheidend, da die Ausgaben innerhalb von `LangChain` komplex sein können.

## Wozu braucht man den Parser?
Man kann den Parser z.B. in einem der folgenden Szenarien einsetzen.

* **Standard-String-Ausgabe**: Wenn ein LLM oder eine Kette einen reinen Textstring als Ergebnis liefern soll und man keine weitere Strukturierung (z.B. JSON, Listen, ect.) benötigt oder erwartet. Das ist wohl der häufigste Anwendungsfall.

* **Endpunkt einer Kette**: Oft ist der Parser das letzte Glied in einer `LangChain` Expression Language Kette (LCEL). Dann nimmt der Parser die Rohausgabe des vorherigen Schritts (z.B. die Antwort eines LLMs) und stellt sicher, dass sie als einfacher String an den Benutzer oder den nächsten Prozess übergeben wird.

* **Lesbarkeit**: Auch wenn eine LLM-Ausgabe oft bereits ein Text ist, kann das explizite Hinzufügen des `StrOutputParser()` die Absicht verdeutlichen, dass man eine reine String-Ausgabe erwartet. Es ist auch eine Form der Typsicherung im Kontext `LangChain`. 

* **Kombination mit anderen Parsern (implizit)**: Wenn man komplexere Parser wie `JsonOutputParser` oder `CommaSeparatedListOutputParser` verwendet, ist der `StrOutputParser` oft implizit der Ausgangspunkt. Die LLM-Ausgabe ist zunächst ein String, der dann widerum von den spezialisierten Parsern weiterverarbeitet wird. 

In der [LangChain Dokumentation](https://python.langchain.com/api_reference/core/output_parsers.html) findet man noch viele weitere Parser.

## Wie verwendet man den `StrOutputParser`?
Der `StrOutputParser()` hat eine Methode namens `parse()`, die einen String als Eingabe erwartet und diesen String dann unverändert zurückgibt. Im Kontext der Chains, kann man ihn z.B. wie folgt verwenden. Das Beispiel ist ggf. nicht ausführbar, weil man noch einen API-Key angeben muss. Das kann man z.B. mittels [[Keyring_de|Keyring]] umsetzen.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Ein einfaches Prompt-Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfreicher Assistent."),
    ("user", "{input}")
])

# Ein LLM-Modell
llm = ChatOpenAI(model="gpt-4o", temperature=0) # Verwende dein bevorzugtes Modell

# Die Kette
chain = prompt | llm | StrOutputParser()

# Aufruf der Kette
response = chain.invoke({"input": "Was ist die Hauptstadt von Frankreich?"})
print(response)
# Erwartete Ausgabe: "Die Hauptstadt von Frankreich ist Paris." (oder ähnlich)
```


Im Beispiel generiert `prompt` einen Prompt-String. `llm` nimmt diesen Prompt entgegen und gibt eine Modellantwort (ein `AIMessage`-Objekt, das einen String enthält) zurück. `StrOutputParser()` nimmt diesen String aus dem `AIMessage`-Objekt und gibt ihn als reinen Python-String zurück.

## Was ist noch wichtig?

* **Standardverhalten**: In vielen einfachen `LangChain`-Ketten, insbesondere wenn man nur ein LLM an Ende hat, ist der `StrOutputParser()` oft der implizite Standard-Parser, wenn man keinen anderen explizit angibt. `LangChain` versucht, die Ausgabe des LLM in einen String zu wandeln, wenn kein spezifischer Parser vorhanden ist. Man gibt ihn in aller Regel aber dennoch an, um die Absicht zu verdeutlichen.

* **Vergleich mit anderen Parsern**: Der `StrOutputParser()` steht im Gegensatz zu anderen Output-Parsern, die eine spezifische Struktur aus der LLM-Ausgabe extrahieren müssen:
  * **JsonOutputParser**: Erwartet JSON-formatierten Text und parst ihn in ein Python-Dictionary oder eine Liste.
  * **CommaSeparatedListOutputParser**: Erwartet eine durch Kommas getrennte Liste und parst sie in eine Python-Liste von Strings.
  * usw. usw.

* **Error Handling**: Der `StrOutputParser()` hat, weil er die Eingabe unverändert zurückgibt, keine spezielle Fehlerbehandlung für falsch formatierte Ausgaben. Wenn die LLM-Antwort nicht ist, was man erwartet, wird sie dennoch einfach als String zurückgegeben. Eine Fehlerbehandlung müsste dann im Anschluss passieren.

* **Simplicity is Key**: Die Stärke des `StrOutputParser()` liegt in seiner Einfachheit. Dieser Parser ist der Baustein für alle Szenarien, in denen man einfach nur einen Text als Ausgabe benötigt, ohne zusätzlicher Transformationen.

**Zusammenfassend** kann man sagen, ist der `StrOutputParser()` ein grundlegendes, unverzichtbares Werkzeug in LangChain, um die rohe Textausgabe von LLMs zu handhaben und sicherzustellen, dass Ketten ein sauberes String-Ergebnis liefern.