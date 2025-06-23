---
tags: ["LangChain", "LLM", "Python"]
author: CKe
---

# `LangChain`'s `BaseOutputParser`-Klasse

Die `BaseOutputParser`-Klasse ist das Fundament aller Output Parser in LangChain. Sie definiert, wie die Rohtextausgabe eines Sprachmodells (LLM) in ein nützliches, strukturiertes Format umgewandelt wird. Jeder spezialisierte Parser, wie der [[StrOutputParser]] oder der `JsonOutputParser`, erbt von ihr und implementiert die `parse`-Methode. Diese nimmt den LLM-Text und wandelt ihn z.B. in einen String, ein JSON-Objekt oder eine Liste um.

Der `BaseOutputParser` ermöglicht eine nahtlose Integration in `LangChain`-Ketten und ist wichtig, wenn man eine benutzerdefinierte Logik für die Verarbeitung der Modellantworten benötigt. So kann man aus Text handhabbare Daten bekommen.