from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 


def cosine2 (X,Y) :
    # Program to measure the similarity between  
    # two sentences using cosine similarity. 
    
    # X = input("Enter first string: ").lower() 
    # Y = input("Enter second string: ").lower() 
    # X ="I love horror movies"
    # Y ="Lights out is a horror movie"
    X=X
    Y=Y
    
    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
    
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
    
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    
    f1 = len(X.split())
    f2 = len(Y.split())
     
    # f2 = cosine * 100 * (f1 + f2)
    f2 = cosine * (f1 + f2)
     
     
    if f1 != 0 : 
        f1 = f2 / (2*f1)
    
    # print("similarity: ", (f1)) 
    return f1

def create_cosine_2_features(df): 
   cosine_2_values = []
   
   for i in df.index:
      if df.loc[i,'Class'] > -1:
         # get texts to compare
         answer_text = df.loc[i, 'Text']
         answer_filename = df.loc[i, 'File'] 
         source_filename = answer_filename
         source_filename = "source" + answer_filename[6:]     
         source_df = df.query('File == @source_filename')
         source_text = source_df.iloc[0].at['Text']

         cosineValue = cosine2(answer_text, source_text)
         cosine_2_values.append(cosineValue)
      else:
         cosine_2_values.append(-1)

   print('COSINE_2 features created!')
   return cosine_2_values

# text1 = "Kartik Vyas studies at IITJ"
# text2 = "Kartik Vyas is an Undergrad student at IITJ"

# print(cosine2(text1,text2))