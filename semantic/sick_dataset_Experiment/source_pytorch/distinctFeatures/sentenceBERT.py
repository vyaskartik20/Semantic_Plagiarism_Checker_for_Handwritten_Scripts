# pip install sentence-transformers
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
import math
model = SentenceTransformer('bert-base-nli-mean-tokens')

sentences = ["I ate dinner.",
             "We had a three-course meal.",
             "Brad came to dinner with us.",
             "He loves fish tacos.",
             "In the end, we all felt like we ate too much.",
             "We all agreed; it was a magnificent evening."]


sentence_embeddings = model.encode(sentences)

# print('Sample BERT embedding vector - length', len(sentence_embeddings[0]))
# print('Sample BERT embedding vector - note includes negative values',
#       sentence_embeddings[0])

query = "I had pizza and pasta"
query_vec = model.encode([query])[0]


for sent in sentences:
    sim = cosine_similarity(query_vec.reshape(
        1, -1), model.encode([sent])[0].reshape(1, -1))
    print("Sentence = ", sent, "; similarity = ", sim)
