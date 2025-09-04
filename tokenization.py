import tiktoken

encoder=tiktoken.encoding_for_model('gpt-4o')

print(encoder.n_vocab ) #vocab size for gpt-40 == 200019(200k)

text='the cat sat on the mat'
tokens=encoder.encode(text)

print("Tokens", tokens)  #Tokens [3086, 9059, 10139, 402, 290, 2450]

decoded= encoder.decode([3086, 9059, 10139, 402, 290, 2450])

print('the decoded value is: ', decoded)

