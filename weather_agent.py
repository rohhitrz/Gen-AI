from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()

client=OpenAI()

def run_command(command):
    result=os.system(command=command)
    return result

# print(run_command("ls"))

def get_weather(city:str):
    print(f'🔨: tool called for {city}')
    url=f"https://wttr.in/{city}?format=%C+%t"
    response=requests.get(url)
   
    if response.status_code==200:
     return f"the weather in the ${city} is {response.text}"
    
    return "something went wrong"

def add(x,y):
      print(f'🔨: tool called for to add {x} and {y}')
      return x+y
    


available_tools={
    "get_weather":{
        "fn": get_weather,
        "description":"takes a city name as an input and retuns current weather for the city"
    },
    "run_command":{
        "fn":run_command,
        "description":"Takes a command as input to execute on system and returns output"

    },
    # "add":{
    #     "fn": add,
    #     "description":"takes two numbers and add them up and returns this sum"
    # }
}

system_prompt=f'''
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
- get_weather:takes a city name as an input and retuns current weather for the city
- run_command: Takes a command as input to execute on system and returns output



Example:
User Query: what is the weather of New York
Output: {{"step":"plan", "content":"the user is interested in weather data of new york" }}
Output: {{"step":"plan", "content":"from the available tool I should call get_weather" }}
Output: {{"step":"action", "function":"get_weather", "input": "new york" }}
Output: {{"step":"observe", "output":"12 Degree celsius" }}
Output: {{"step":"output", "content":"the weather for New York seems to be 12 Degrees." }}

'''
messages=[
    {'role':'system', 'content':system_prompt}
]

user_query=input('> ')
messages.append({'role':'user', 'content':user_query} )

while True:
    response=client.chat.completions.create(

        model='gpt-4o',
        response_format={"type":"json_object"},
        messages=messages

    )

    parsed_output=json.loads(response.choices[0].message.content)
    messages.append( {"role":"assistant", "content": json.dumps(parsed_output)} )

    if parsed_output.get('step')=="plan":
        print(f"🧠:{parsed_output.get('content')} ")
        continue
    
    if parsed_output.get('step')=="action":
        tool_name=parsed_output.get("function")
        tool_input=parsed_output.get("input")

        if available_tools.get(tool_name,False):
            output=available_tools[tool_name].get('fn')(tool_input)

            messages.append({'role':'assistant',"content": json.dumps({
                "step":"observe", "output":output
            }) })
        
            continue

    if parsed_output.get('step')=="output":
         print(f"🤖:{parsed_output.get('content')} ")
         break


    


# response=client.chat.completions.create(
#     model='gpt-4o',
#     response_format={"type":"json_object"},
#     messages=[
#          {'role':'system', 'content':system_prompt},
#         {'role':'user', 'content':'what is the current weather of Bengaluru'},
#         {'role':'assistant', 'content':'what is the current weather of Bengaluru'},
#         {'role':'assistant', 'content':json.dumps({
#             "step":"plan", "content":"the user is interested in the current weather data of Bengaluru"
#         })},
#         {'role':'assistant', 'content':json.dumps({
#             "step":"plan", "content":"from the available tool I should call get_weather"
#         })},
#         {'role':'assistant', 'content':json.dumps({
#             "step": "action", "function": "get_weather", "input": "Bengaluru"
#         })},
#         {'role':'assistant', 'content':json.dumps({
#             "step": "observe", "output": "31 degree celsius."
#         })},
#         ]

# )

# print(response.choices[0].message.content)