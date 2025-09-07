from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client=OpenAI()

def get_weather(city:str):
    return "24 degrees"

system_prompt='''
you are a helpful AI assistant who is specialized in resolving user query.
you work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution, based on the planning select the relevent tool from the available tool. and based on the tool selection you perform an action to call the tool. 
wait for observation and based on observation from the tool call resolve the user query.

Rules:
-Follow the output JSON Format.
-Always perform one step at a time and wait for next input.
-carefully analyze the user query.

Output JSON format:
{{
"step": "string",
"content":"string",
"function": "The name of Function if the step is action",
"input": "the input parameter for the  function"

}}

Available Tools:


Example:
User Query: what is the weather of New York
Output: {{"step":"plan", "content":"the user is interested in weather data of new york" }}
Output: {{"step":"plan", "content":"from the available tool I should call get_weather" }}
Output: {{"step":"action", "function":"get_weather", "input": "new york" }}
Output: {{"step":"observe", "output":"12 Degree celsius" }}
Output: {{"step":"output", "content":"the weather for New York seems to be 12 Degrees." }}

'''

response=client.chat.completions.create(
    model='gpt-4o',
    response_format={"type":"json_object"},
    messages=[
         {'role':'system', 'content':system_prompt},
        {'role':'user', 'content':'what is the current weather of Bengaluru'},
        {'role':'assistant', 'content':'what is the current weather of Bengaluru'},
        {'role':'assistant', 'content':json.dumps({
            "step":"plan", "content":"the user is interested in the current weather data of Bengaluru"
        })},
        {'role':'assistant', 'content':json.dumps({
            "step":"plan", "content":"from the available tool I should call get_weather"
        })},
        {'role':'assistant', 'content':json.dumps({
            "step": "action", "function": "get_weather", "input": "Bengaluru"
        })},
        {'role':'assistant', 'content':json.dumps({
            "step": "observe", "output": "31 degree celsius."
        })},
        

        ]


)

print(response.choices[0].message.content)