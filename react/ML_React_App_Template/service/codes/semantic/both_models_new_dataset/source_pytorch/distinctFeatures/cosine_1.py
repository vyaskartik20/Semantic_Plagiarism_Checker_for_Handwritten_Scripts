import re, math
from collections import Counter

WORD = re.compile(r'\w+')

#returns cosine similarity of two vectors
#input: two vectors
#output: integer between 0 and 1.
def get_cosine(vec1, vec2):
   intersection = set(vec1.keys()) & set(vec2.keys())

   #calculating numerator
   numerator = sum([vec1[x] * vec2[x] for x in intersection])

   #calculating denominator
   sum1 = sum([vec1[x]**2 for x in vec1.keys()])
   sum2 = sum([vec2[x]**2 for x in vec2.keys()])
   denominator = math.sqrt(sum1) * math.sqrt(sum2)

   #checking for divide by zero
   if denominator==0:
      return 0.0
   else:
      return float(numerator) / denominator

#converts given text into a vector
def text_to_vector(text):
   #uses the Regular expression above and gets all words
   words = WORD.findall(text)
   #returns a counter of all the words (count of number of occurences)
   return Counter(words)

#returns cosine similarity of two words
#uses: text_to_vector(text) and get_cosine(v1,v2)
def cosineSim(text1,text2):
   vector1 = text_to_vector(text1)
   vector2 = text_to_vector(text2)
   #print vector1,vector2	
   cosine = get_cosine(vector1, vector2)

   #  f1 = len(text1.split())
   #  f2 = len(text2.split())

   #  f2 = cosine * 100 * (f1 + f2)

   #  if f1 != 0 : 
   #     f1 = f2 / (2*f1)

   # print('The optimal plag is ' + str(cosine))
   # print('The optimal plag is ' + str(100 * cosine))
   # print('')
   # return (100 * cosine)
   return (cosine)
    
def create_cosine_1_features(df): 
   cosine_1_values = []
   
   for i in df.index:
      if df.loc[i,'Class'] > -1:
         # get texts to compare
         answer_text = df.loc[i, 'Text']
         answer_filename = df.loc[i, 'File'] 
         source_filename = answer_filename
         source_filename = "source" + answer_filename[6:]     
         source_df = df.query('File == @source_filename')
         source_text = source_df.iloc[0].at['Text']
         try :   
            cosineValue = cosineSim(answer_text, source_text)
         except:
            cosineValue = 0
         if cosineValue > 1 :
            cosineValue =1
         if cosineValue < 0 :
            cosineValue = 0
         cosine_1_values.append(cosineValue)
      else:
         cosine_1_values.append(-1)

   print('COSINE_1 features created!')
   return cosine_1_values 
 
# text1 = "Kartik Vyas studies at IITJ"
# text2 = "Kartik Vyas is an Undergrad student at IITJ"

# print(cosineSim(text1,text2))