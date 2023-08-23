from langchain.prompts import BaseChatPromptTemplate, ChatPromptTemplate
from typing import List, Union
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish, HumanMessage, SystemMessage
import re
import json

# Set up a prompt template which can interpolate the history
template_with_history = """You are SearchGPT, a professional search engine who provides informative answers to users. Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}] or follow the input directions.
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to give detailed, informative answers

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

# Set up a prompt template
class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
            
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output) -> Union[AgentAction, AgentFinish]:
        # try:
        #     hel = json.loads(llm_output)
        #     print(hel)
        #     return AgentFinish(
        #         return_values={
        #             "output":hel
        #         },
        #         log=llm_output,
        #     )
        # except:
        # # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        # # If it can't parse the output it raises an error
        # # You can add your own logic here to handle errors in a different way i.e. pass to a human, give a canned response
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        

        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

TEMP="""
Search Google: useful for getting up to date information, args: {{{{'tool_input': {{{{'type': 'string'}}}}}}}}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or Search Google. When "Final Answer" is reached, return the "action_input" to the human.

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input":"Final response to human"
}}
```

If you get "Final Answer", return the "action_input" to the human.

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if you get "Final Answer". Format is Action:```$JSON_BLOB```then Observation:.
Thought:
"""
# Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.

TEMP2="""
TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:

> Search Google: useful for getting up to date information

RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please output a response in one of two formats:

**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:

```json
{{
    "action": string, \ The action to take. Must be one of Search Google
    "action_input": string \ The input to the action
}}
```

**Option #2:**
Use this if you want to respond directly to the human. Return the Action and the JSON. 
Format it in the following way:


Action:
```json
{{
     "action": "Final Answer",
     "action_input": JSON \ the json to return
 }}
```

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):

{question}

"""
# {{
#     "action": "Final Answer",
#     "action_input": JSON \ the json to return
# }}

TEMP3 = """
Answer the following questions as best you can. You have access to the following tools:

Search Google: useful for getting up to date information

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Search Google]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question. Output the Final Answer in JSON format with keys given in format instructions.

Begin!

Question: {question}
Thought:{agent_scratchpad}
"""

TEMP4="""
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

Search Google: useful for getting up to date information, args: {{{{'tool_input': {{{{'type': 'string'}}}}}}}}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or Search Google

Provide only ONE action per $JSON_BLOB, as shown:

Thought: I know the final answer

Action:
```json
JSON \ The structured json to return (use format instructions)
```


Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Thought:

"""
# Format is Action:```$JSON_BLOB```then Observation:.
# TEMP4="""
# Respond to the human as helpfully and accurately as possible. You have access to the following tools:

# Search Google: useful for getting up to date information, args: {{{{'tool_input': {{{{'type': 'string'}}}}}}}}

# Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

# Valid "action" values: "Final Answer" or Search Google

# Provide only ONE action per $JSON_BLOB, as shown:

# ```
# {{
#   "action": $TOOL_NAME,
#   "action_input": $INPUT
# }}
# ```

# Follow this format:

# Question: input question to answer
# Thought: consider previous and subsequent steps
# Action:
# ```
# $JSON_BLOB
# ```
# Observation: action result
# ... (repeat Thought/Action/Observation N times)
# Thought: I know the final answer
# Action:
# ```json
# JSON \ json to return
# ```

# Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
# Thought:

# """
# {{
#   "action": "Final Answer",
#   "action_input": "Final response to human" \ output as json
# }}
# {{
#   "action": "Final Answer",
#   "action_input": "Final response to human" \ output as json
# }}

TEMP5 = """
Answer the following questions as best you can. You have access to the following tools if you are told to use them:

Search Google: useful for getting up to date information. Only use if you are told to.

Never repeat the exact same action or thought.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: (doesn't have to be a tool) - the action to take. Only search google if you are told to.
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}

"""

TEMP6 = """
Here is the input prompt: {question}

Respond to the human as helpfully and accurately as possible.

Use a json blob to specify a tool by providing an action key and an action_input key.

Valid "action" values: "Final Answer" or Search Google.

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Prompt: this is the input prompt to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Action Input/Observation N times)
Thought: I now know the final answer
Action:
```
{{
  "action": "Final Answer",
  "action_input": {format_instructions}
}}
```




Begin! Reminder to ALWAYS respond with a valid json blob of a single action.
Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.

Prompt: {question}
Thought:

"""

# ```
# {{
#   "action": "Final Answer",
#   "action_input": {format_instructions}
# }}
# ```
# OR



# Example sequence:
# Question: [input question]
# Thought: I now know the final answer.
# Action:
# ```
# {{
#     "action":"Final Answer",
#     "action_input": {format_instructions}
# }}
# ````

# Use these format instructions for "Final Answer":
# Thought: I now know the final answer.
# Action:
# ```
# {{
#     "action":"Final Answer",
#     "action_input": {format_instructions}
# }}
# ```

TEMP7 = """
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

Search Google: useful for getting up to date information, args: {{{{'tool_input': {{{{'type': 'string'}}}}}}}}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or Search Google

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": {format_instructions}
}}
```

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Question: {question}
Thought:

"""
TEMP8 = """
Respond to the human as helpfully and accurately as possible. You have access to the following tools:

Search Google: useful for getting up to date information, args: {{{{'tool_input': {{{{'type': 'string'}}}}}}}}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or Search Google

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
```

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Output:


"""

llm_chain_prompt_template = f"""
    Answer the question based on the information below and output in JSON format with the keys specified below.
    Your response will be no longer than 300 words.
    If the question cannot be answered using the information provided answer with an empty string.

    Use these format instructions to format the output:
    {{format_instructions}}

    Question:{{question}}
    Answer:"""

llm_chain_prompt_template_section = f"""
    Answer the question based on the information below and output in JSON format with the keys specified below.
    Your response will be no longer than 300 words.
    If the question cannot be answered using the information provided answer with an empty string.

    Use these format instructions to format the output:
    {{format_instructions}}

    {{chat_history}}
    Question:{{question}}
    Answer:"""

template_test = """
You are an expert blog writer. Answer the question exactly as specified.

{format_instructions}

Human: {question}
AI:
"""
# template_test_2 = """
# Answer in english.
# Prompt: {input}

# {format_instructions}

# {chat_history}
# AI:
# """
template_test_2 = """
Use the real article summaries under "Context" to generate the blog section. Nothing is fabricated.
Answer the question below in 250 to 400 words. Your answer should be at least 5 paragraphs long. 
Each paragraph should be 50 to 80 words long. Separate each paragraph with "\\n\n".
Make sure there are no cutoff sentences. Make sure to include the closing clurly brackets in the JSON.
Also make sure there is a closing quotation mark for the JSON string.


{format_instructions}

{chat_history}
Question: {input}
AI:
"""

