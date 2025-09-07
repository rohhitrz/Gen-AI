import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

messages = [
    { "role": "system", "content": system_prompt },
]


query = input("> ")
messages.append({ "role": "user", "content": query })


while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({ "role": "assistant", "content": json.dumps(parsed_response) })

    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get("content")}")
        continue
    
    print(f"🤖: {parsed_response.get("content")}")
    break


 

# result=client.chat.completions.create(
#     model='gpt-4',
#     # response_format= {"type",'json_schema'},
#     messages=[
#         {'role':'system', 'content':system_prompt},
#         {'role':'user', 'content':'what is 3+4*5'},
#         {'role':'assistant', 'content':json.dumps({"step": "analyse", "content": "the user is asking for operation for that involves both addition and multiplication, so I need to follow order of operation."})},
#         {'role':'assistant', 'content': json.dumps({
#             "step":'think', 'content':"According to the BODMAS principle to solve this equation, multiplication should be done before addition"
#         })},
#         {'role':'assistant', 'content': json.dumps({
#             "step":'output', 'content':"In the equation, if we follow BODMAS, we should do the multiplication first which is 4*5=20 and then add the result to 3, so it would be 3+20"
#         })},
#         {'role':'assistant', 'content': json.dumps({
#             "step":'output', 'content':"In the equation, if we follow BODMAS, we should do the multiplication first which is 4*5=20 and then add the result to 3, so it would be 3+20"
#         })},
#         {'role':'assistant', 'content': json.dumps({
#             "step":'validate', 'content':"By performing calculation using the BODMAS principle, 3+4*5 turns into 3+20 which equal to 23"
#         })},
#         {'role':'assistant', 'content': json.dumps({
#             "step":'result', 'content':"The result of the operation 3+4*5 is 23"
#         })},

#     ] 
# )

# print(result.choices[0].message.content)
