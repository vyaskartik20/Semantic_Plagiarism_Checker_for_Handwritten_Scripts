texts = []

for x in range(1,6):
    with open(str(x)+'.txt','r') as file:
        Str = file.read()
        texts.append(Str)
#print(texts)
#print(len(texts))
#print(texts[0])