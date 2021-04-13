import os

N_GRAM_2 = 0.15
N_GRAM_3 = 0.25
N_GRAM_4 = 0.2
COSINE_2 = 0.05
DOCISM_NLTK = 0.05 
LCS = 0.1
SEQUENCE_MATCHER = 0.2
# codes.real_plag.

from codes.real_plag.distinctFeatures import cosine_2

# from codes.real_plag. import cosine_1
# from distinctFeatures import cosine_2
# from distinctFeatures import cosine_trigram
from codes.real_plag.distinctFeatures import docism_nltk
# from distinctFeatures import jaccard_trigram
from codes.real_plag.distinctFeatures import lcs
from codes.real_plag.distinctFeatures import ngram
# from distinctFeatures import phrase_nltk_1
# from distinctFeatures import phrase_nltk_2
from codes.real_plag.distinctFeatures import rabin_karp_2
from codes.real_plag.distinctFeatures import sequence_matcher
# from distinctFeatures import tensorflow_sentence_embedding

def make_features(text1,text2) :     
    arr = []
    
    # val = cosine_trigram.similarity(text1,text2)
    # arr.append(val)
    # print(f" cosine trigram  : {val}")


    ngram_range = {2,3,4}
    
    for n in ngram_range:
        val = ngram.calculate_containment_individual(text1,text2,n)
        arr.append(val)
        # print(f" ngram  {n}  : {val}")

    # val = cosine_1.cosineSim(text1,text2)
    # arr.append(val)
    # print(f"  cosine1 : {val}")

    val = cosine_2.cosine2(text1,text2)
    arr.append(val)
    # print(f" cosine2  : {val}")

    val = docism_nltk.docism(text1,text2)
    arr.append(val)
    # print(f" docism_nltk  : {val}")

    # val = jaccard_trigram.similarity(text1,text2)
    # arr.append(val)
    # print(f" jaccard_trigram  : {val}")

    val = lcs.lcs_norm_word(text1,text2)
    arr.append(val)
    # print(f" lcs  : {val}")


    val = sequence_matcher.similarity(text1,text2)
    arr.append(val)
    # print(f" sequecne_matcher  : {val}")

    return arr

def main() :
    
    files = os.listdir('docs_backup')

    for file1 in files :
        file1 = 'docs_backup/' + file1
        text1 = open(file1, errors='ignore').read()
        for file2 in files  :
            file2 = 'docs_backup/' + file2
            if file1 != file2 :                
                text2 = open(file2, errors = 'ignore').read()
                result = make_features(text1,text2)
                
                ans = 0
                
                for res in result :
                    if res > 1:
                        res =1
                    # if res :
                    #     res =0
                
                ans = ans + result[0] * N_GRAM_2
                ans = ans + result[1] * N_GRAM_3
                ans = ans + result[2] * N_GRAM_4
                ans = ans + result[3] * COSINE_2
                ans = ans + result[4] * DOCISM_NLTK
                ans = ans + result[5] * LCS
                ans = ans + result[6] * SEQUENCE_MATCHER
                
                print(f"{file1} and {file2}  ::   {ans} ")
        print()
        print()
            
            
def web_real_similarity(text1,text2) :
    result = make_features(text1,text2)
                
    ans = 0
    
    for res in result :
        if res > 1:
            res =1
        # if res :
        #     res =0
    
    print(f'ngram2 :  {result[0]} ') 
    print(f'ngram3 :  {result[1]} ') 
    print(f'ngram4 :  {result[2]} ') 
    print(f'cosine2 :  {result[3]} ') 
    print(f'docismNLTK :  {result[4]} ') 
    print(f'lcs :  {result[5]} ') 
    print(f'seqmatcher :  {result[6]} ') 
    
    
    ans = ans + result[0] * N_GRAM_2
    ans = ans + result[1] * N_GRAM_3
    ans = ans + result[2] * N_GRAM_4
    ans = ans + result[3] * COSINE_2
    ans = ans + result[4] * DOCISM_NLTK
    ans = ans + result[5] * LCS
    ans = ans + result[6] * SEQUENCE_MATCHER
    
    # print(f"{file1} and {file2}  ::   {ans} ")
    # print(ans)
    ans = ans*100
    return ans
                    
if __name__ == '__main__':
    # main()

    text1 = "kartik vyas is a boy njn b jkds nvnre eebcb ioner bb"
    text2 = "kartik vyas is not a girl student at indian fner jfnre ffner "

    web_real_similarity(text1,text2)