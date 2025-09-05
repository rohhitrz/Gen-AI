from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client=OpenAI()
system_prompt='''
you are an AI assistant who is expert in breaking down complex problems and then resolve the userr query.

For the given user input, analyze the input and break down the problem step by step.

atLeast think 5-6 steps on how to solve problem before solving it down.

the steps are you get a user input, you analyze, you think, you think again think for several times and return an output for several times and then return an output with  explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output",  "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. always perform one step at a time and wait for next input
3. carefully analyze the user query 

Output Format:
{{step: 'string', content:'string'}}

Example:

input: what is 2+2.
output: {{step: "analyse", content: "Alright!, the user is interested in maths query and he is asking a basic arthematic operation"}}

output: {{step: "think", content: "To perform the addition you must go from left to right and add all the operands"}}

output: {{step: "output",content:"4" }}
output: {{step: "validate", "content": "seems like 4 is correct answer for 2+2"} }
output: {{step: "result", "content": "2+2 is 4 and that is calculated by adding all numbers"} }
'''





result=client.chat.completions.create(
    model='gpt-4',
    # response_format= {"type",'json_schema'},
    messages=[
        {'role':'system', 'content':system_prompt},
        {'role':'user', 'content':'what is 3+4*5'},
        {'role':'assistant', 'content':json.dumps({"step": "analyse", "content": "the user is asking for operation for that involves both addition and multiplication, so I need to follow order of operation."})},
        {'role':'assistant', 'content': json.dumps({
            "step":'think', 'content':"According to the BODMAS principle to solve this equation, multiplication should be done before addition"
        })},
        {'role':'assistant', 'content': json.dumps({
            "step":'output', 'content':"In the equation, if we follow BODMAS, we should do the multiplication first which is 4*5=20 and then add the result to 3, so it would be 3+20"
        })},
        {'role':'assistant', 'content': json.dumps({
            "step":'output', 'content':"In the equation, if we follow BODMAS, we should do the multiplication first which is 4*5=20 and then add the result to 3, so it would be 3+20"
        })},
        {'role':'assistant', 'content': json.dumps({
            "step":'validate', 'content':"By performing calculation using the BODMAS principle, 3+4*5 turns into 3+20 which equal to 23"
        })},
        {'role':'assistant', 'content': json.dumps({
            "step":'result', 'content':"The result of the operation 3+4*5 is 23"
        })},

    ] 
)

print(result.choices[0].message.content)
