from difflib import SequenceMatcher

def similarity(answer, source):
    # source = purifyText(source)
    f1 = (SequenceMatcher(None,answer,source).ratio())*100
    c1 = len(answer.split())
    c2 = len(source.split())
    
    c3=((f1/200) * (c1+c2))
    f2 = (c1+c2)/(2*c1)
    f3=(f1*f2)
    
    # print('the plag is :') 
    # print(f3)
    return f3