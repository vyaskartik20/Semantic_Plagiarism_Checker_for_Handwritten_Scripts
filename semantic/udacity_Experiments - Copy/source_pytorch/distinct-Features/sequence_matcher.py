from difflib import SequenceMatcher

def similarity(answer, source):
    # source = purifyText(source)
    # f1 = (SequenceMatcher(None,answer,source).ratio())*100
    f1 = (SequenceMatcher(None,answer,source).ratio())
    c1 = len(answer.split())
    c2 = len(source.split())
    
    c3=((f1/200) * (c1+c2))
    f2 = (c1+c2)/(2*c1)
    f3=(f1*f2)
    
    # print('the plag is :') 
    # print(f3)
    return f3

# text1 = "Kartik Vyas studies at IITJ"
# text2 = "Kartik Vyas is an Undergrad student at IITJ"

# print(similarity(text1,text2))