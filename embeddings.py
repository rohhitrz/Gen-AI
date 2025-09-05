from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client=OpenAI()

text="Biryani is famous In hyderabad,India"

response=client.embeddings.create(
    input=text,
    model='text-embedding-3-small'
)

print('vector embeddings', response.data[0].embedding);