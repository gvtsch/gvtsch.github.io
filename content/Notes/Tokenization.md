---
title: Tokenisierung - Wie Computer Sprache "lesen"
date: 2025-07-22
tags: [ml, dl, python, llm, nlp, transformer, tokenization, embedding]     # TAG names should always be lowercase
toc: true
---

# Tokenisierung - Wie Computer Sprache "lesen"

Bevor Large Language Models (LLMs) wie ChatGPT Text verstehen oder generieren können, muss dieser in ein Format umgewandelt werden, mit dem der Computer arbeiten kann. Genau hier kommt die Tokenisierung ins Spiel – ein wichtiger erster Schritt in der Verarbeitung natürlicher Sprache (Natural Language Processing, NLP).

## Was ist Tokenisierung?

Tokenisierung ist der Prozess, bei dem ein fortlaufender Text in kleinere Einheiten zerlegt wird, die wir Tokens nennen. Ein Token kann ein einzelnes Wort, ein Satzzeichen, ein Teil eines Wortes (Subwort) oder sogar ein einzelnes Zeichen sein. Die genaue Art der Tokens hängt von der gewählten Tokenisierungsstrategie ab.

Stell dir vor, du hast einen langen Satz. Für einen Computer ist das zunächst nur eine Abfolge von Zeichen. Durch die Tokenisierung verwandeln wir diesen Satz in eine geordnete Liste von "Bausteinen", die dann weiterverarbeitet werden können.

## Und wozu das ganze?

Computer verstehen Text selbstverständlich nicht so, wie wir Menschen es können. Sie benötigen eine numerische Darstellung. Durch die Tokenisierung wird der Text in diskrete Einheiten heruntergebrochen. Diese Tokens können dann wiederum in sogenannte [[Embeddings]] gewandelt werden. [[Embeddings]] sind numerische Vektordarstellungen der Textschnipsel oder Tokens, mit denen NLP-Modelle arbeiten und komplexe Sprachmuster verarbeiten können.

Die Tokenisierung ist entscheidend, weil sie ...

* **... Text für Modelle aufbereitet**: Sprachmodelle operieren nicht direkt mit rohem Text. Tokens sind die numerischen Eingaben, die sie benötigen.
* **... Komplexität reduziert**: Statt unendlich vieler möglicher Zeichenkombinationen zu verarbeiten, arbeiten Modelle mit einer begrenzten Anzahl von Tokens.
* **... Bedeutung bewahrt**: Gute Tokenizer versuchen, die semantische und syntaktische Integrität der Sprache so gut wie möglich zu erhalten.
* **... Effizienz ermöglicht**: Durch die Segmentierung in überschaubare Einheiten wird die Verarbeitung durch das Modell effizienter.

## Warum unterschiedliche Arten von Tokens?

Warum werden Texte unterschiedlich tokenisiert? Das hängt stark von der Aufgabe und dem verwendeten Sprachmodell ab. Die folgenden Beispiele und Extremfälle sollten verdeutlichen, dass es Gründe für die unterschiedlichen Strategien gibt.

* **Worttokenisierung**: Die einfachste Form, bei der der Text anhand von Leerzeichen und Satzzeichen in Wörter unterteilt wird. Aus z.B. `Hallo Welt!` wird dann `["Hallo", "Welt", "!"]`.
  * **Vorteile**: Intuitiv, Tokens sind leicht verständlich.
  * **Nachteile**: Umgang mit unbekannten Wörtern (Out-Of-Vocabulary - OOV), große Vokabulare, Morpheme (Wortstämme, Vorsilben, Endungen) werden nicht berücksichtigt.
* **Zeichen-Tokenisierung**: Jedes Zeichen wird zu einem Token.
  * **Vorteile**: Kleinster möglicher Vokabularumfang, keine OOV-Probleme
  * **Nachteile**: Sehr lange Sequenzen, verliert semantische Informationen auf Wortebene, erfordert komplexere Modelle, um längere Abhängigkeiten zu lernen.
* **Subword(Teilwort)-Tokenisierung**: Das ist die am häufigsten verwendete Methode in modernen NLP-Modellen (wie z.B. bei Transformer-Architekturen wie BERT, GPT, etc.). Hier werden Wörter in kleinere, häufig vorkommende Teilwörter zerlegt. Beispiele für Algorihtmen sind [Byte Pair Encoding (BPE)](https://huggingface.co/learn/llm-course/chapter6/5), [WordPiece](https://huggingface.co/learn/llm-course/chapter6/6) oder [Unigram](https://huggingface.co/learn/llm-course/chapter6/7) Language Model.
  Der Kern dieser Methoden liegt in einem cleveren Mechanismus, der als iterative Zusammenführung oder Substitution verstanden werden kann. Algorithmen wie BPE beginnen typischerweise mit einem Vokabular, das aus einzelnen Zeichen besteht. Dann durchsuchen sie den Text nach dem am häufigsten vorkommenden Paar von benachbarten Zeichen (oder bereits gebildeten Subwörtern). Dieses Paar wird zu einem neuen, einzelnen Token zusammengeführt und das Vokabular entsprechend erweitert. Anschließend werden alle Vorkommen dieses Paares im Text durch das neue, zusammengeführte Token ersetzt (substituiert). Dieser Prozess wird so lange wiederholt, bis eine vordefinierte Vokabulargröße erreicht ist oder keine häufigen Paare mehr gefunden werden. Auf diese Weise entstehen Tokens, die von einzelnen Zeichen bis hin zu ganzen Wörtern reichen können.
  * **Vorteile**:
    * **Reduziert OOV-Probleme**: Seltene und unbekannte Wörter können aus bekannten Subwords zusammengesetzt werden. So könnte z.B. `Unbekanntwort` zu `["Un", "bek", "annt", "wort"]` tokenisiert werden. Das kann man auch [hier](https://platform.openai.com/tokenizer) schön testen. Dort wird `Unbekanntwort` eben genau das ;)
    * **Optimierter Speicherbedarf und Effizienz**: Durch die Zusammenführung häufiger Zeichenkombinationen zu einzelnen Subwort-Tokens wird die Gesamtanzahl der Tokens in einer Textsequenz oft erheblich reduziert. Das führt zu kürzeren Eingabesequenzen für das Modell, was wiederum den Rechen- und Speicherbedarf während des Trainings und der Inferenz minimiert. Ein kleineres, aber  effektives Vokabular ist speichereffizienter als ein riesiges Wortvokabular.
    * **Kompromiss zwischen Wort- und Zeichen-Tokenisierung**: Kleinere Vokabulare als bei Wort-Tokenisierung, aber sinnvollere Einheiten als bei Zeichen-Tokenisierung.
    * **Umgang mit Morphemen**: Kann gemeinsame Morpheme erkennen und nutzen. Z.B. wird `running` und `runs` zu `["run", "##ning"], ["run", "##s"]`
  * **Nachteile**: Tokens sind nicht immer intuitive Wörter, die Segmentierung ist modellabhängig.

## Wichtige Aspekte bei der Tokenisierung

Wenn man über Tokenisierung spricht, besonders im Kontext moderner Sprachmodelle, gibt es manche Begriffe, die man mal gehört haben sollte. 

* **Vokabular**: Eine Liste aller einzigartigen Tokens, die der Tokenizer kennt und verwenden kann. Jedes Token im Vokabular erhält eine eindeutige numerische ID.
* **Mapping von Text zu IDs**: Der Tokenizer wandelt den rohen Text schrittweise in eine Abfolge seiner identifizierten Tokens um, und diese Tokens werden dann in ihre entsprechenden numerischen IDs umgewandelt.
* **Sonder-Tokens (Special Tokens)**: Modelle verwenden oft spezielle Tokens für bestimmte interne Zwecke, die dem Text zusätzliche Struktur oder Informationen verleihen:
  * `[CLS]`: Klassifikationstoken (bei BERT oft der erste Token in einer Sequenz, dessen Embedding für Klassifikationsaufgaben verwendet wird).
  * `[SEP]`: Trenn-Token, um verschiedene Segmente oder Sätze innerhalb einer Eingabesequenz zu separieren.
  * `[PAD]`: Füll-Token, um alle Sequenzen in einem Batch auf eine einheitliche Länge zu bringen. Dies ist notwendig für die effiziente Verarbeitung in neuronalen Netzen.
  * `[UNK]`: Unbekanntes Token (Unknown Token), ein Platzhalter für Wörter oder Subwörter, die nicht im Vokabular des Tokenizers enthalten sind.



## Beispiel in Python mit TikTokenizer (tiktoken)

`tiktoken` ist eine schnelle Open-Source-Tokenisierungs-Bibliothek von OpenAI, die für Modelle wie bswp. `GPT-3` oder `GPT-4` verwendet wird. Die Bibliothek implementiert eine Variante des Byte Pair Encoding.

Mit `pip install tiktoken` lässt es sich installieren. 


```python
import tiktoken

# 1. Den passenden Encoder laden (z.B. für GPT-4)
# 'cl100k_base' wird von gpt-4, gpt-3.5-turbo und text-embedding-ada-002 genutzt.
encoding = tiktoken.get_encoding("cl100k_base")

text_example = "Hallo Welt! Tokenisierung ist super."

print(f"Originaltext: '{text_example}'")
print("-" * 30)

# 2. Text in Token-IDs umwandeln (Encoding)
token_ids = encoding.encode(text_example)

print(f"Token-IDs: {token_ids}")
print(f"Anzahl der Tokens: {len(token_ids)}")
print("-" * 30)

# 3. Token-IDs zurück in Text umwandeln (Decoding)
decoded_text = encoding.decode(token_ids)

print(f"Zurückdecodierter Text: '{decoded_text}'")
print("-" * 30)

# 4. Die einzelnen Tokens (als Strings) anzeigen
print("Einzelne Tokens:")
for token_id in token_ids:
    token_str = encoding.decode([token_id]) # Jede ID einzeln decodieren
    print(f"  ID: {token_id}, Token: '{token_str}'")
```
```bash
  Originaltext: 'Hallo Welt! Tokenisierung ist super.'
  ------------------------------
  Token-IDs: [79178, 46066, 0, 9857, 285, 37716, 6127, 2307, 13]
  Anzahl der Tokens: 9
  ------------------------------
  Zurückdecodierter Text: 'Hallo Welt! Tokenisierung ist super.'
  ------------------------------
  Einzelne Tokens:
    ID: 79178, Token: 'Hallo'
    ID: 46066, Token: ' Welt'
    ID: 0, Token: '!'
    ID: 9857, Token: ' Token'
    ID: 285, Token: 'is'
    ID: 37716, Token: 'ierung'
    ID: 6127, Token: ' ist'
    ID: 2307, Token: ' super'
    ID: 13, Token: '.'
```
    
### Interpretation des Beispiels

Der Output zeigt, wie der Eingabetext in einzelne Tokens zerlegt und anschließend wieder zusammengesetzt wird:

* **Originaltext und Zurückdecodierter Text**: Wie erwartet sind die Texte nach Encodieren (in IDs umwandeln) und Decodieren (zurück in Text umwandeln) identisch. Das zeigt, dass keine Informationen verloren gegangen sind.
* **Token-IDs und Anzahl der Tokens**: Der Beispieltext wurde in 9 Tokens zerlegt und jedes Token hat eine eindeutige ID erhalten.
* **Einzelne Token**: 
  * `Hallo` und `!` sind eigenständige Tokens
  * ` Welt` beginnt mit einem Leerzeichen. Das ist typisch für Subword-Tokenisierung wie BPE. Leerzeichen werden oft mit dem nachfolgenden Wort zusammengefasst, um die Anzahl der Tokens zu optimieren und die Rekonstruktion des Originaltextes zu erleichtern.
  * Das Wort `Tokenisierung` wird in ` Token`, `is` und `ierung` zerlegt. Ein schönes Beipiel für Subword-Tokenisierung: Wort zu verwenden, wird es in häufiger vorkommende Silben oder Wortteile aufgeteilt. Dies hilft, das Vokabular zu reduzieren und ermöglicht es dem Modell, auch unbekannte oder seltene Wörter zu verarbeiten, indem es deren bekannte Subwort-Bestandteile interpretiert.
  * ` ist`, ` super` und `.` folgen ähnlichen Mustern, wobei die Wörter ist und super ebenfalls mit einem vorangestellten Leerzeichen tokenisiert werden.

Das Beispiel verdeutlicht das Schlüsselkonzept, wie große, moderne Sprachmodelle Text nicht immer als ganze Wörter betrachten, sondern in kleinere, statistisch optimierte Einheiten aufteilen, um Effizienz und Verständnis zu maximieren.