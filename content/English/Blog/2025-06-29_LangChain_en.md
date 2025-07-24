---
title: What exactly is `LangChain`?
date: 2025-06-29
tags: ["python", "langchain", "langgraph", "ml", "llm", "nlp", "agent", "multi-agent"]
toc: True
draft: false
author: CKe
---

# What exactly is LangChain?

Among other things, I am currently working with `LangChain`. And I am trying to record my thoughts here in some form.

## Introduction

LangChain is a powerful framework that combines the integration and interaction of large language models (LLMs) with external data and tools. LLMs are inherently limited in their knowledge to the data they were trained on and can rarely access external information directly or perform complex actions. This is exactly where LangChain comes in.

The framework overcomes these limitations by giving LLMs the ability to interact with the outside world. Imagine you want to develop a chatbot that can not only answer general questions based on its internal knowledge, but also retrieve information from specific sources such as Wikipedia or your own internal documents and remember what has been said so far. Without LangChain, you would have to build everything yourself, integrate APIs, write conversation logic, etc. LangChain greatly simplifies this complex task by allowing you to use pre-built chains, memory, and tools.

In addition, LangChain promotes enormous flexibility and modularity in your projects. Instead of relying on a single, often overloaded “super prompt,” LangChain enables the development of intelligent agents that can each be assigned specific tasks. This makes it much easier to develop complex LLM applications in a structured and maintainable way.

### Advantages
The advantages include:
* **Modularity**: Similar to a building block principle, different components can be used and exchanged.
* **Flexibility**: LangChain is very flexible and adaptable to a wide variety of use cases.
* **Abstraction**: LangChain hides some functionalities behind interfaces, thereby reducing complexity.
* **Extensibility**: Thanks to its modular design, it is easy to integrate additional tools or data sources.
* **Use cases**: 
  * Chatbots
  * Question-and-answer systems using, for example, your own files
  * Agents that perform tasks
  * ...

## Basic concepts in `LangChain`

### Large Language Models (LLMs)

For virtually every LLM application, you need... surprise, surprise, an LLM. LLMs are models that can understand and generate text. Well-known LLMs include OpenAI's GPT models, Google's Gemini, and open-source models such as Llama or Mistral from France. 

`LangChain` provides a unified interface for interacting with different LLMs without having to change your own code.

Here's a really simple example of how that might look:

```python
from langchain_openai import OpenAI

llm = OpenAI(temperature=0.7)
print(llm.invoke("What is the name of the most beautiful city in Germany?"))
```

Or if you want to interact with Mistral:

```python
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(temperature=0.7)
print(llm.invoke("What is the name of the most beautiful city in Germany?"))
```

Basically, not much more than the import and the class used changes. Everything else is implemented in the background by `LangChain`.

What I have omitted in both cases is the `API-KEY`. You usually cannot integrate with LLMs without such an `API key`. If you have such a key, you can integrate and use it via [[dotenv]] or [[keyring]], for example.

In fact, many more parameters can be configured. I have only adjusted the [[`temperature`]] parameter here. For Mistral, information on the other parameters can be found in this [LangChain documentation](https://python.langchain.com/api_reference/mistralai/chat_models/langchain_mistralai.chat_models.ChatMistralAI.html). For OpenAI, you can find similar information in this [LangChain documentation](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html).

### Prompts and `PromptTemplates`

In the example above, the LLM is called with the command `invoke`. This means that the model is actively used or executed to perform a specific task or obtain a response. 
In the example, we pass the question “What is the most beautiful city in Germany?” to the LLM. This question is a prompt, and we expect the LLM to respond with a textual answer to our question. The quality of the answers depends heavily on the quality of the prompts. It is easy to imagine that without further criteria, the answer will also vary for us humans. 

This prompt is also, of course, extremely static. Sometimes you want to make your prompts dynamic (e.g., insert a country into the question). This is where LangChain's PromptTemplate comes into play. These are templates that contain placeholders that are filled with values at runtime. This allows you to reuse your prompt, create consistency, and reduce errors.

A `PromptTemplate` could look like this, for example:

```python
from langchain.prompts import PromptTemplate

template = “”"You are a helpful assistant who summarizes information. Summarize the following text on the topic {topic}. The text is {text}. Output the summary in {language}.“”"

prompt = PromptTemplate(
    input_variables=[“topic”, ‘test’, “language”],
    template=template
)

print(prompt.format(
    topic="Artificial Intelligence",
    text="Artificial Intelligence (AI) deals with the simulation of human intelligence in machines...",
    language="German"))
```

The finished prompt looks like this:

```bash
You are a helpful assistant who summarizes information. Summarize the following text on the topic of artificial intelligence. The text is: Artificial intelligence (AI) deals with the simulation of human intelligence in machines.... Output the summary in German.
```

The individual placeholders have been filled with content. This prompt can then be used to invoke agents or chains.

### Chains

A chain is a link between components such as `PromptTemplate` and LLMs. They enable multiple steps to be executed in succession, with the output of one step being used as input for the next.
This makes it relatively easy to set up pipelines for LLM operations. An LLM chain is, for example, the most basic chain that connects a prompt with an LLM.

Chains allow you to structure your code easily and simplify often complex workflows.

An LLM chain could look like this, for example (integrate the API key as usual, e.g., via [[keyring]]):

```python
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.7)

summarize_template = "Summarize the following text: {text}"
summarize_prompt = PromptTemplate.from_template(summarize_template)

summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

long_text = "Künstliche Intelligenz (KI), englisch artificial intelligence, daher auch artifizielle Intelligenz (AI), ist ein Teilgebiet der Informatik, das sich mit der Automatisierung intelligenten Verhaltens und dem maschinellen Lernen befasst. Der Begriff ist schwierig zu definieren, da es verschiedene Definitionen von Intelligenz gibt. [...] Der Begriff artificial intelligence (künstliche Intelligenz) wurde 1955 geprägt von dem US-amerikanischen Informatiker John McCarthy im Rahmen eines Förderantrags an die Rockefeller-Stiftung für das Dartmouth Summer Research Project on Artificial Intelligence, einem Forschungsprojekt, bei dem sich im Sommer 1956 eine Gruppe von 10 Wissenschaftlern über ca. 8 Wochen mit der Thematik befasste."
summary = summarize_chain.invoke({"text": long_text})
print(summary['text'])
```
_Text from [Wikipedia](https://de.wikipedia.org/wiki/K%C3%BCnstliche_Intelligenz)_

Since the input text is not particularly long, the summary will hardly be much shorter, but I think it will suffice to understand the principle. So here is the summary in question:

```bash
KI oder AI ist ein Teilgebiet der Informatik, das sich mit der Automatisierung intelligenten Verhaltens und dem maschinellen Lernen beschäftigt. Der Begriff ist schwer zu definieren, da es verschiedene Definitionen von Intelligenz gibt. Der Begriff wurde 1955 von John McCarthy geprägt und im Rahmen eines Forschungsprojekts im Sommer 1956 von einer Gruppe von 10 Wissenschaftlern untersucht. 
```

#### What is `Invoke`?

_Invoking_ a chain or agent in `LangChain` means that you pass an input (usually a dictionary, as above) to the object and receive an immediate response. The input is sent to the chain, the language model processes this request (using memory or a tool, if necessary), and you receive the result directly.

In short, `invoke()` is the method used to send requests to a chain or agent and receive the response synchronously.

### Agents and Tools

Agents and tools ensure that LLMs can act more “intelligently.” An agent decides which tools to use and in what order based on the current problem. Functions that an agent can call to perform external actions include, for example, a Google or Wikipedia search, a database query, calling an API, etc. Langchain offers many ready-made tools for this purpose and also allows you to create your own.

An abstract example: You ask the agent, “What will the weather be like tomorrow?” 
This may be followed by the following sequence:
* Agent recognizes: Need weather information
* Agent selects the “weather tool”
* Agent calls up the tool with “Hamburg, tomorrow”
* The “weather tool” returns data
* Agent formulates the answer for the user with LLT

A less abstract but shorter example in Python:

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import OpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

llm = OpenAI(temperature=0)

# Tool
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [wikipedia]

# Prompt für ReAct Agent
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({"input": "Wer ist der aktuelle Bundeskanzler von Deutschland?"}))
```

The output shows how the ReAct agent proceeds. It determines that it should use Wikipedia, searches a few pages, and finally delivers the correct result (as of 2025-06-29). I have shortened the output of the individual Wikipedia pages because it is irrelevant for understanding.

```bash
> Entering new AgentExecutor chain...
 I should use Wikipedia to find the answer.
Action: wikipedia
Action Input: "Bundeskanzler Deutschland"Page: Deutschlandlied
Summary: The "Deutschlandlied", officially titled "Das Lied der Deutschen", is a German poem written by August Heinrich Hoffmann von Fallersleben . A popular song [...]

Page: Chancellor of Germany
Summary: The chancellor of Germany, officially the federal chancellor of the Federal Republic of Germany, is the head of the federal government of Germany. [...] The current officeholder is Friedrich Merz of the Christian Democratic Union, sworn in on 6 May 2025.]

Page: Friedrich Merz
Summary: Joachim-Friedrich Martin Josef Merz (born 11 November 1955) is a German politician serving as Chancellor of Germany since 6 May 2025. [...]
Final Answer: The current Bundeskanzler of Germany is Friedrich Merz.

> Finished chain.
{'input': 'Wer ist der aktuelle Bundeskanzler von Deutschland?', 'output': 'The current Bundeskanzler of Germany is Friedrich Merz.'}
```

Incidentally, a [[2025-07-14-ReAct_en|ReAct]] agent is used at the top. A [[2025-07-14-ReAct_en|ReAct]] agent combines “reasoning” (logical inference) and “acting” (action). It uses language models to consider, in several steps, which actions (e.g., tool calls) are necessary to achieve a goal. In doing so, it alternates between thinking and acting.

### Memory

LLMs are stateless by default, meaning they forget everything after each request. Memory modules in `LangChain` make it possible to remember past conversations or states. This enables chatbots, personalized applications, or, for example, multi-layered, complex interactions.

There are many types of storage, e.g., for databases or Redis. I would like to list two here.
* `ConversationBufferMemory`: Stores the entire conversation
* `ConversationSummaryMemory`: Summarizes the conversation if it becomes too long.

A `ConversationChain` with `ConversationBufferMemory` could look like this:

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI

llm = OpenAI(temperature=0.7, api_key=api_key)
memory = ConversationBufferMemory()

conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

print(conversation.invoke({"input": "Hallo, mein Name ist Christoph"}))
print(conversation.invoke({"input": "Wie geht es dir heute?"}))
print(conversation.invoke({"input": "Erinnerst du dich an meinen Namen?"}))
print(conversation.invoke({"input": "Erzähle mir etwas über Python"}))
```

If you run the above lines in a Jupyter Notebook, for example, you will get a visually enhanced conversation history enriched with additional information. If, on the other hand, you only want to view questions and answers, the following lines will help.

```python
for message in memory.chat_memory.messages:
    print(f"{message.type}: {message.content}")
```

It then delivers the following result.

```bash
human: Hallo, mein Name ist Christoph
ai:  Hallo Christoph! Schön dich kennenzulernen. Mein Name ist AI, was für Artificial Intelligence steht. Ich bin ein Programm, das entwickelt wurde, um menschenähnliche Gespräche zu führen und Fragen zu beantworten. Wie kann ich dir heute weiterhelfen?
human: Wie geht es dir heute?
ai:  Mir geht es gut, danke der Nachfrage. Ich bin ein Computerprogramm, also habe ich keine körperlichen Empfindungen wie Menschen. Aber meine Programmierung läuft einwandfrei, also bin ich glücklich. Wie geht es dir?
human: Erinnerst du dich an meinen Namen?
ai:  Ja, dein Name ist Christoph. Ich habe eine Datenbank mit allen Informationen, die du mir im Laufe unserer Gespräche gibst, und ich erinnere mich an alles, was du mir gesagt hast.
human: Erzähle mir etwas über Python
ai:  Python ist eine beliebte Programmiersprache, die in den 1990er Jahren von Guido van Rossum entwickelt wurde. Sie ist bekannt für ihre einfache Syntax und flexible Anwendungsbereiche. Viele große Unternehmen wie Google und Instagram nutzen Python für ihre Anwendungen. Es ist auch eine der am häufigsten verwendeten Sprachen für künstliche Intelligenz und maschinelles Lernen. Hast du noch weitere Fragen zu Python oder möchtest du mehr darüber erfahren?
```

What immediately stands out: The question about my name can still be answered even after further questions. In this way, an LLM, which, as mentioned, is “stageless,” could be turned into a chatbot.

#### Transferring the `ConversationChain` to the LLM

To connect a `ConversationChain` to an LLM, the LLM object is passed as an argument when the chain is created. The chain then takes over communication with the model. In the example above, the LLM (`llm=llm`) is passed directly to the `ConversationChain`. The chain then takes care of generating prompts, saving the history, and retrieving the responses from the LLM. Interaction with the LLM then takes place via methods such as `invoke`. 

This makes the chain the central building block that connects the LLM, memory, and logic.

## Application example

I would like to show further application examples in additional examples.

### Document retrieval (Retrieval Question Answering - [[RAG_en|RAG]])

LLMs only have knowledge up to their training date and no specific company or project data. If you want to change that, RAG comes into play. With it, you can “extend” the LLM with relevant external documents to answer specific questions.

The workflow can then look something like this:
* **Load documents**: PDFs, text files, databases, etc.
* **Split texts**: Break large documents down into smaller, manageable chunks.
* **Embedding**: The text chunks are converted into numerical vectors.
* **Vector database (Vector Store)**: Stores the previously converted vectors for a fast similarity search (e.g., [[cosine similarity]]) in vector databases (e.g., `Chroma`, `FAISS`, `Pinecone`)
* **Query**: 
  * User asks a question
  * Question is “embedded”
  * The most similar chunks from the vector database are retrieved
* **LLM response**: The retrieved chunks and the question are presented to the LLM, which then generates an informed response.

The advantages are obvious: the answers are based on my data, hallucinations are reduced, and current information can be retrieved.

What might this look like in code?
In the following code snippet, I import a PDF. It is [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) [cs.CL]. I also query Wikipedia on the topic. Once without a function, once embedded in a function. And I load an API key with Keyring.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_core.documents import Document
import os

# API-Key laden
import keyring
api_key = keyring.get_password("openai_api_key", "default")

# OpenAI Schnittstelle vorbereiten
llm = OpenAI(temperature=0, api_key=api_key)
embeddings = OpenAIEmbeddings(api_key=api_key)

# PDF laden
loader = PyPDFLoader(r"Attention_is_all_you_need_1706.03762v7.pdf")
docs = loader.load()

# Embeddings und Vektordatenbank erzeugen
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

# Chain vorbereiten
qa_chain = RetrievalQA.from_chain_type(
	llm=llm,
	chain_type="stuff",
	retriever=vectorstore.as_retriever())

# Frage stellen
query = "Was bedeutet Attention?"
response = qa_chain.invoke({"query": query})
print(f"Ergebnis PDF: {response['result']}")
``` 

The above lines result in the following output.

```bash
Ergebnis PDF:  Attention ist eine Funktion, die eine Abfrage und eine Reihe von Schlüssel-Wert-Paaren auf einen Ausgang abbildet, wobei alle Elemente Vektoren sind. Der Ausgang wird als gewichtete Summe berechnet.
```

However, as mentioned above, we can also consult Wikipedia on this topic:

```python
# Wikipedia Schnittstelle vorbereiten
def load_from_wikipedia(query, lang='en', load_max_docs=2):
    from langchain.document_loaders import WikipediaLoader

    loader = WikipediaLoader(
        query=query,
        lang=lang,
        load_max_docs=load_max_docs,
    )
    data = loader.load()
    return data

# Wikipedia befragen
data = load_from_wikipedia("Attention (Machine Learning)", lang='de', load_max_docs=3)
print(f"Ergebnis Wikipedia: {data[0].page_content[:250]}")
```

The output follows immediately. For the first output—we have instructed our agent to search for the 3 best matches—I output the first $500$ characters.

```bash
Ergebnis Wikipedia: Ein Transformer ist eine von Google entwickelte Deep-Learning-Architektur, die einen Aufmerksamkeitsmechanismus (englisch Attention) integriert. Dabei wird Text durch Worteinbettung in numerische Darstellungen in Form von Vektoren umgewandelt. Dies kann z. B. dazu benutzt werden, Text von einer Sprache in eine andere zu übersetzen (siehe auch Maschinelle Übersetzung). Dazu wird ein Transformer mittels maschinellem Lernen anhand einer (großen) Menge von Beispieltexten trainiert, bevor das trainie
```

The above article obviously also deals with the attention mechanism. Without delving further into the content, this is the best result according to the agent.

The second-best result deals with LLMs. However, I will only quote the first 250 characters:

```python
print(f"Ergebnis Wikipedia: {data[1].page_content[:250]}")
```

```bash
Ergebnis Wikipedia: Ein Large Language Model, kurz LLM (englisch, teilweise übertragen großes Sprachmodell), ist ein Sprachmodell, das sich durch seine Fähigkeit zur Textgenerierung auszeichnet. Es handelt sich um ein computerlinguistisches Wahrscheinlichkeitsmodell, da
``` 

And the third result seems to deal with `Tensorflow`.

```python
print(f"Ergebnis Wikipedia: {data[2].page_content[:250]}")
```

```bash
Ergebnis Wikipedia: TensorFlow ist ein Framework zur datenstromorientierten Programmierung. Populäre Anwendung findet TensorFlow im Bereich des maschinellen Lernens. Der Name TensorFlow stammt von Rechenoperationen, welche von künstlichen neuronalen Netzen auf mehrdimen
``` 

Once the Wikipedia results have been loaded, you can now perform various further steps, for example:

1. **Summarize**  
The contents of the Wikipedia articles can be automatically summarized using an LLM to present the most important information in a compact form.
2. **Compare**  
You can compare the contents of different articles to identify differences or similarities. 
3. **Answer questions (QA)**  
You can ask specific questions about the loaded Wikipedia articles using RetrievalQA or your own chain that uses the articles as a knowledge base.

  ```python
  from langchain.chains import RetrievalQA
  from langchain_community.vectorstores import FAISS
  from langchain_openai import OpenAIEmbeddings

  # Embeddings für Wikipedia-Artikel erzeugen
  wiki_vectorstore = FAISS.from_documents(data, embedding=embeddings)
  wiki_qa_chain = RetrievalQA.from_chain_type(
     llm=llm,
     chain_type="stuff",
     retriever=wiki_vectorstore.as_retriever()
  )

  frage = "Was ist ein Transformer im Kontext von Machine Learning?"
  antwort = wiki_qa_chain.invoke({"query": frage})
  print(f"Antwort: {antwort['result']}")
  ```

4. **Further processing**
- Extract keywords or entities.
- Create mind maps or visualizations.
- Combine Wikipedia content with other data sources.

This allows you to flexibly reuse the loaded Wikipedia data (or other data) for various NLP tasks.

### Chatbots

Another example that we have all encountered at some point is the chatbot. The aim of a chatbot is to enable interactive, context-sensitive conversation. 

This requires, among other things, a memory (for the conversation history) and often also a retriever (to answer specific questions). Combining the two, we can also refer to a “ConversationalRetrievalChain.” The chatbot can then remember the conversation and search for answers in documents.

We can reuse the code from the previous examples and add “ConversationalRetrievalChain” and “ConversationBufferMemory” to:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_core.documents import Document
import os

# API-Key laden
import keyring
api_key = keyring.get_password("openai_api_key", "default")

# OpenAI Schnittstelle vorbereiten
llm = OpenAI(temperature=0, api_key=api_key)
embeddings = OpenAIEmbeddings(api_key=api_key)

# PDF laden
loader = PyPDFLoader(r"C:\Users\...\Attention_is_all_you_need_1706.03762v7.pdf")
docs = loader.load()

# Embeddings und Vektordatenbank erzeugen
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

memory = ConversationBufferMemory(
    memory_key="chat_history", # Wichtig: Key muss 'chat_history' sein
    return_messages=True
)

# Erstelle die ConversationalRetrievalChain
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)


# Interagiere mit dem Chatbot
response1 = conversation_chain.invoke({"question": "Was ist Attention?"})
print("User: Was ist Attention?")
print("Bot:", response1['answer'])

response2 = conversation_chain.invoke({"question": "Wer ist der Autor?"})
print("\nUser: Wer ist der Autor?")
print("Bot:", response2['answer'])

response3 = conversation_chain.invoke({"question": "Erinnerst du dich, worüber wir zuerst gesprochen haben?"})
print("\nUser: Erinnerst du dich, worüber wir zuerst gesprochen haben?")
print("Bot:", response3['answer']) # Hier sollte es "langchain" sein, da im Memory
```

The output will then look as follows:

```bash
User: Was ist Attention?
Bot:  Attention is a function that maps a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors. It is used in neural network architectures, such as the Transformer, to connect the encoder and decoder and improve performance in sequence transduction tasks. It allows the network to focus on specific parts of the input and make connections between distant dependencies.

User: Wer ist der Autor?
Bot: 
Die Autoren des Transformer-Modells sind Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser und Illia Polosukhin.

User: Erinnerst du dich, worüber wir zuerst gesprochen haben?
Bot: 
Attention ist eine Funktion, die eine Anfrage und eine Reihe von Schlüssel-Wert-Paaren auf einen Ausgang abbildet. Dabei sind die Anfrage, die Schlüssel, die Werte und der Ausgang alle Vektoren. Der Ausgang wird als gewichtete Summe berechnet.
```

You can recognize the activity of the bot (the `ConversationalRetrievalChain`) by the fact that the answers to specific questions (e.g., about the meaning of “attention” or the authors) come directly and precisely from your PDF document. The function of the buffer (the `ConversationBufferMemory`) is evident because the bot remembers previous conversation topics (“Do you remember what we talked about first?”) and responds based on them.

It seems to be working!

### Data analysis and generation

A few scenarios—without code—for how LangChain can be used for data analysis and generation:
* LangChain can also be used to summarize large data sets (e.g., log files or customer reviews).
* Extract specific information from unstructured text.
* Generate reports or descriptions based on structured data.
* Code generation or explanation
* ...

Another example, but also only theoretical, is an agent that can access CSV files and answer questions about them by generating and executing Python code. Tools such as `PythonREPLTool` or `PandasDataFrame` could then be used. 

The possibilities are almost endless ;)

## Summary

`LangChain` is a powerful framework for creating “intelligent” LLM-based applications. It simplifies complex processes through modular components.

It can be used almost anywhere: customer service, education, content creation, data analysis, etc.

I will continue to explore this topic. There is still a lot to learn about callbacks, custom components, integrations, and LangGraph.

If you have any questions, comments, suggestions, or have found any errors, please don't hesitate to contact me :)
