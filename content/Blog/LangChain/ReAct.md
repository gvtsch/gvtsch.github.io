---
title: What exactly is ReAct?
date: 2025-07-14
tags: ["python", "langchain", "ml", "llm", "nlp", "agent", "react"]
toc: True
draft: false
author: CKe
---

# ReAct - Reasoning and Acting

ReAct (Reasoning + Acting) is an approach that enables large language models (LLMs) to perform both logical thinking (reasoning) and actions (acting) in an integrated process. ReAct combines the ability of LLMs to generate chains of reasoning ([[Prompt-Techniques|Chain-of-Thought]]) with the ability to perform task-specific actions, such as retrieving information, calling APIs, or using external tools.

## Process

* The agent receives a task.
* He thinks ("Thought").
* He decides on an action ("Action").
* He receives a result ("Observation").
* He repeats the steps until the task is solved.

```mermaid
flowchart TD
    A[Receive task] --&gt; B[Thought: Think]
    B --&gt; C[Action: Select tool/action]
    C --&gt; D[Observation: Receive result]
    D --&gt; E{Goal achieved?}
    E -- No --&gt; B
    E -- Yes --&gt; F[Give answer]
```

## Key features of ReAct:
* **Reasoning**: The model explains its thought processes by generating step-by-step considerations. This improves the transparency and traceability of decisions.
* **Actions (Acting)**: In addition to reasoning, the model performs concrete actions, such as retrieving information or interacting with an environment.
* **Nesting**: ReAct combines thinking and acting in a nested manner. The model can switch between reasoning and action to solve complex tasks efficiently.

## Advantages of ReAct:

* **Improved problem solving**: By combining thinking and acting, the model can handle * complex tasks that pure thinking or acting alone could not solve.
* **Explainability**: The reasoning traces make the model's decisions comprehensible.
* **Flexibility**: ReAct can be used in various areas of application, e.g., in automation, decision-making, or interaction with external tools.

Unlike agents that only reason (think) or only act (perform tasks), ReAct agents combine both approaches. This allows them to solve more complex problems, adapt to new situations, and provide more reliable and explainable results.

---

## Example in the [[What is LangChain]] environment:

A ReAct model could answer a question by first thinking about the question, then querying a search engine, analyzing the results, and finally providing an informed answer.

In the following, I would like to program a small ReAct agent that can execute Python code, query Wikipedia, or start an Internet search. To do this, I will define tools that this agent is then allowed to use. I will not show the entire code, but only the parts that are helpful for understanding. The boilerplate code can be handled by programming copilots anyway.

First, the question arises: what makes an agent a ReAct agent?

### What makes an agent a ReAct agent?

The agent becomes a ReAct agent through the strategic combination of three core elements that interact in the [[What is LangChain]] environment:

* **The ReAct principle (Reasoning + Acting)**: This is the fundamental theoretical framework. It guides the agent to proceed in an iterative cycle of "thinking" (Thought), "choosing an action" (Action), and "observing the result" (Observation). The agent becomes a ReAct agent because it uses this specific way of thinking and acting to solve problems.
* **A special prompt (e.g., `hub.pull('hwchase17/react'))`: This prompt is absolutely crucial. It is not a mere instruction, but a detailed guide that teaches the LLM how to execute the ReAct process. It typically contains:
    * Examples ([[Prompt-Techniques|Few-shot]] examples): These show the LLM what the "Thought" process should look like, how to correctly formulate an "Action" (tool call), and how to interpret the "Observation" in order to arrive at the next "Thought."
    * Format specifications: These define the exact text format in which the agent should output its thoughts and actions (e.g., "Thought: ...", "Action: ...", "Action Input: ...").
    Without this prompt, which is specifically tailored to ReAct, the LLM would not know how to execute this complex cycle of thought and action. It acts as the "instruction manual" for the LLM to behave like a ReAct agent.
  * The following are instructions on how to import the prompt:
    ```python
    from langchain import hub
    hub.pull('hwchase17/react')

    print(prompt.input_variables)
    print(prompt.template)
    ```

    And the content:
    
    ```bash
    ['agent_scratchpad', 'input', 'tool_names', 'tools']
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    ```

* **Orchestration by `create_react_agent` and `AgentExecutor`**: These functions from [[What is LangChain]] are the technical "conductors":
  * `create_react_agent` takes the LLM, the available tools, and the prompt tailored to ReAct and configures the agent accordingly.
  * The `AgentExecutor` is the control center that controls the ReAct process step by step. It sends the prompt to the LLM, reads its response (to recognize thoughts, actions, and their inputs), executes the desired action using the appropriate tool, and returns the result ('observation') to the LLM. This cycle repeats until the agent has found a final answer.

Now let's move on to the tools.

### Tools

In the context of large language models, and ReAct agents in particular, tools are external functions or interfaces that give the LLM capabilities beyond its pure text generation and language comprehension function. While LLMs excel at recognizing patterns in text and generating coherent responses, they have well-known inherent limitations:

* **Knowledge base**: LLMs' knowledge is limited to the data they were trained on. This knowledge quickly becomes outdated in today's world.
* **Logic and precise calculations**: LLMs can make mistakes and hallucinate when performing complex mathematical calculations or adhering to strict logical rules. 
* **Interaction with the outside world**: LLMs cannot directly access the internet, call APIs, or perform actions in real-world systems.

This is where tools come into play. They extend LLMs and agents with "senses" and "capabilities" by allowing the agent to perform specific external tasks. A ReAct agent decides, based on its reasoning, which tool is best suited to answer an intermediate question or solve a problem, and then processes the results of the tool.

#### Python REPL

Here’s how you define the Python REPL tool for your agent.

```python
python_repl = PythonREPLTool()
python_repl_tool = Tool(
    name = 'Python REPL',
    func = python_repl.run,
    description = 'Useful when you need to run Python code. Input should be a valid Python expression or statement.',
)
```

The Python REPL (Read-Eval-Print Loop) tool allows the agent to execute Python code directly. This is particularly useful for precise calculations, data manipulation, testing hypotheses, or complex logical operations where an LLM alone might be prone to errors. It acts as a "calculator on steroids" and "logic engine." We will see this in the example below.

#### Wikipedia

Here’s how you set up the Wikipedia tool.

```python
api_wrapper = WikipediaAPIWrapper()
wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)
wikipedia_tool = Tool(
    name = 'Wikipedia',
    func = wikipedia.run,
    description = 'Useful for getting information about a topic. Input should be a question or topic.',
)
```

The Wikipedia tool allows the agent to access Wikipedia's extensive and structured knowledge base. It is ideal for retrieving more or less reliable, factual information on a wide range of topics that may not be included in the LLM's original training dataset or may be out of date. The agent uses it to quickly get an overview of a topic or to check specific facts.

#### TavilySearchResults

Here’s how you configure the Tavily Search tool.


```python
search = TavilySearchResults(
    max_results=1,
    include_answer=True,
)

tavily_tool = Tool(
    name='Tavily Search',
    func=search.run,
    description='Useful for getting information from the web. Input should be a question or topic.',
)
```

The Tavily Search Tool allows agents to search for real-time information on the internet. Unlike Wikipedia, which accesses curated knowledge, Tavily is particularly valuable for finding highly topical information, news, or specific website content that is constantly changing. It expands the agent's ability to interact with the dynamic world outside its training data and is often the first choice for general information gathering.

#### Additional tools

Beyond the three tools discussed, there are of course many more. LLM agents can access a wide range of specialized tools to expand their core capabilities. These include, for example, access to academic databases, financial APIs, or product databases for targeted searches. Data analysis tools such as SQL interaction or spreadsheet APIs are also conceivable. For interaction with the environment, they can use email services, calendar APIs, or file system access. Even the direct execution of shell commands or interaction with image generation services is possible. This variety of tools enables agents to solve precise problems, access up-to-date information, and master complex tasks in the real world.

### Combining the tools into an agent

`Tools`, `AgentExecutor`, and `create_react_agent` can be imported from [[What is LangChain]].
```python
from langchain.agents import Tool, AgentExecutor, create_react_agent
```

The tools that the agent is ultimately allowed to use are summarized as such in a list.

```python
tools = [tavily_tool, python_repl_tool, wikipedia_tool]
```

Then the agent is being created:

```python
agent = create_react_agent(llm, tools, prompt)
agent_executer = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
)
```

And finally, you can instruct the agent to create something, search for something, etc. 

```python
question = 'Generate the first 20 Fibonacci numbers.'
output = agent_executer.invoke({
    'input': prompt_template.format(q=question),
})
```

The agent then begins to "think" about how to reach its goal and finally presents its route and the solution.

````bash
> Entering new AgentExecutor chain...
To generate the first 20 Fibonacci numbers, I will write a simple Python function that calculates them. 

Action: Python REPL  
Action Input: `def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence[:n] fibonacci(20)`  
SyntaxError('invalid syntax', ('&lt;string&gt;', 1, 41, 'def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence[:n] fibonacci(20)\n', 1, 44))It seems there was a syntax error in the Python code I attempted to run. I will correct the code and try again to generate the first 20 Fibonacci numbers.

Action: Python REPL  
Action Input: `def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence fib_sequence = fibonacci(20)`  
SyntaxError('invalid syntax', ('&lt;string&gt;', 1, 41, 'def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence fib_sequence = fibonacci(20)\n', 1, 44))It seems that I am encountering a syntax error in the Python code. I will rewrite the function with proper indentation and structure to ensure it runs correctly.

Action: Python REPL  
Action Input: `def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence[:n] fib_sequence = fibonacci(20)`  
SyntaxError('invalid syntax', ('&lt;string&gt;', 1, 41, 'def fibonacci(n): fib_sequence = [0, 1] for i in range(2, n): fib_sequence.append(fib_sequence[-1] + fib_sequence[-2]) return fib_sequence[:n] fib_sequence = fibonacci(20)\n', 1, 44))It appears that I am consistently encountering a syntax error due to the formatting of the code. I will break down the function definition and the call into separate lines to ensure proper execution.

Action: Python REPL  
Action Input: 
```python
def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

fib_sequence = fibonacci(20)
fib_sequence
```

I have successfully generated the first 20 Fibonacci numbers. 

Final Answer: The first 20 Fibonacci numbers are: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181].

> Finished chain.
````

As proof that it does not always generate a Python function:

```python
question = 'Who is the last chancellor of Germany?'
output = agent_executer.invoke({
    'input': prompt_template.format(q=question),
})
```

This leads to the following train of thought (here, the agent first interprets "last chancellor" as "current chancellor" and then corrects its search in the second step):

```bash
> Entering new AgentExecutor chain...
I need to find out who the current chancellor of Germany is, as the question asks for the last chancellor. 

Action: Tavily Search  
Action Input: "current chancellor of Germany 2023"  [{'title': 'Chancellor of Germany - Wikipedia', 'url': 'https://en.wikipedia.org/wiki/Chancellor_of_Germany', 'content': 'The current officeholder is Friedrich Merz of the Christian Democratic Union, sworn in on May 6, 2025.', 'score': 0.6897452}]I have found that the current chancellor of Germany is Friedrich Merz, who was sworn in on May 6, 2025. However, since the question asks for the last chancellor, I need to verify who held the position before him.

Action: Tavily Search  
Action Input: "previous chancellor of Germany before Friedrich Merz"  [{'title': 'List of chancellors of Germany | Names & Years - Britannica', 'url': 'https://www.britannica.com/place/list-of-chancellors-of-Germany-2066807', 'content': 'Konrad Adenauer (1949–63)\n    \n   Ludwig Erhard (1963–66)\n    \n   Kurt Georg Kiesinger (1966–69)\n    \n   Willy Brandt (1969–74)\n    \n   Helmut Schmidt (1974–82)\n    \n   Helmut Kohl (1982–98)\n    \n   Gerhard Schröder (1998–2005)\n    \n   Angela Merkel (2005–21)\n    \n   Olaf Scholz (2021–25)\n    \n   Friedrich Merz (2025– )\n    \n\nThe Editors of Encyclopaedia BritannicaThis article was most recently revised and updated by Amy Tikkanen.\n\nImage 15: Britannica Chatbot logo [...] Philipp Scheidemann (1919)\n    \n   Gustav Bauer (1919–20)\n    \n   Hermann Müller (1920; 1st time)\n    \n   Konstantin Fehrenbach (1920–21)\n    \n   Joseph Wirth (1921–22)\n    \n   Wilhelm Cuno (1922–23)\n    \n   Gustav Stresemann (1923)\n    \n   Wilhelm Marx (1923–25; 1st time)\n    \n   Hans Luther (1925–26)\n    \n   Wilhelm Marx (1926–28; 2nd time)\n    \n   Hermann Müller (1928–30; 2nd time)\n    \n   Heinrich Brüning (1930–32)\n    \n   Franz von Papen (1932)\n    \n   Kurt von Schleicher (1932–33)', 'score': 0.8190992}]I have found that the last chancellor before Friedrich Merz was Olaf Scholz, who served from 2021 to 2025. 

Final Answer: The last chancellor of Germany before Friedrich Merz was Olaf Scholz, who was in office from 2021 to 2025.

> Finished chain.
```

I think it's easy to understand how the ReAct agent works. 

## Summary
In summary, ReAct is a powerful approach that enables large language models to solve complex problems through a dynamic combination of logical thinking and targeted actions. The ability to transparently trace the agent's thought process through thought and action steps is valuable for debugging and crucial for trust in AI systems. And thanks to tools like [[What is LangChain]], the development and deployment of such intelligent agents are becoming increasingly accessible, opening up new possibilities for a wide range of applications.