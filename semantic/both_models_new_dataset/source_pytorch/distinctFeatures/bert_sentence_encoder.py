# pip install sentence-transformers
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
import math
import torch
model = SentenceTransformer('bert-base-nli-mean-tokens')

# sentences = ["I ate dinner.",
#              "We had a three-course meal.",
#              "Brad came to dinner with us.",
#              "He loves fish tacos.",
#              "In the end, we all felt like we ate too much.",
#              "We all agreed; it was a magnificent evening."]


# sentence_embeddings = model.encode(sentences)

# print('Sample BERT embedding vector - length', len(sentence_embeddings[0]))
# print('Sample BERT embedding vector - note includes negative values',
#       sentence_embeddings[0])

# query = "I had pizza and pasta"
# query_vec = model.encode([query])[0]


# for sent in sentences:
#     sim = cosine_similarity(query_vec.reshape(
#         1, -1), model.encode([sent])[0].reshape(1, -1))
#     print("Sentence = ", sent, "; similarity = ", sim)

def similarity(text1, text2) :
    try : 
        vec1 = model.encode([text1])[0]
        vec2 = model.encode([text2])[0]
    except :
        return 0
    sim = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))
    
    return sim


# text1 = "kartik is a student"
# text2 = "kartik studies at college"

# print(similarity(text1,text2))

def create_bert_sentence_encoder_features(df): 
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

        torch.cuda.empty_cache()


    print('bert sentence encodings features created!')
    return sequence_matcher_values