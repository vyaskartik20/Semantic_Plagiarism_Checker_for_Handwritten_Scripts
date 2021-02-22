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

def create_sequence_matcher_features(df): 
    sequence_matcher_values = []

    for i in df.index:
        if df.loc[i,'Class'] > -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            source_filename = answer_filename
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            # value = similarity(answer_text, source_text, False)
            value = similarity(answer_text,source_text)
            
            if value > 1 :
                value =1
            if value < 0 :
                value = 0
            
            sequence_matcher_values.append(value)
        else:
            sequence_matcher_values.append(-1)

    print('sequence_matcher features created!')
    return sequence_matcher_values

# print(similarity(text1,text2))