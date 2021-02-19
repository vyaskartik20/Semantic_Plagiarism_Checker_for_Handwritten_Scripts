import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import numpy as np
from os.path import dirname, join
import re
import math


class PlagiarismChecker:
    def __init__(self, file_a, file_b):
        self.file_a = file_a
        self.file_b = file_b
        self.hash_table = {"a": [], "b": []}
        self.k_gram = 3
        content_a = (self.file_a)
        content_b = (self.file_b)
        self.calculate_hash(content_a, "a")
        self.calculate_hash(content_b, "b")

    # calaculate hash value of the file content
    # and add it to the document type hash table
    def calculate_hash(self, content, doc_type):
        text = self.prepare_content(content)
        text = "".join(text)
        # print(text)

        text = rolling_hash(text, self.k_gram)
        for _ in range(len(content) - self.k_gram + 1):
            self.hash_table[doc_type].append(text.hash)
            if text.next_window() == False:
                break
        # print(self.hash_table)

    def get_rate(self):
        return self.calaculate_plagiarism_rate(self.hash_table)

    # calculate the plagiarism rate using the plagiarism rate formula
    def calaculate_plagiarism_rate(self, hash_table):
        th_a = len(hash_table["a"])
        th_b = len(hash_table["b"])
        a = hash_table["a"]
        b = hash_table["b"]
        sh = len(np.intersect1d(a, b))
        # print(sh, a, b)
        # print(sh, th_a, th_b)

        # Formular for plagiarism rate
        # P = (2 * SH / THA * THB ) 100%
        p = (float( sh)/(th_a)) * 100
        return p

    # get content from file
    def get_file_content(self, filename):
        file = open(filename, 'r+', encoding="utf-8")
        return file.read()

    # Prepare content by removing stopwords, steemming and tokenizing
    def prepare_content(self, content):
        # STOP WORDS
        stop_words = set(stopwords.words('english'))
        # TOKENIZE
        word_tokens = word_tokenize(content)

        filtered_content = []
        # STEMMING
        porter = PorterStemmer()
        for w in word_tokens:
            if w not in stop_words:
                w = w.lower()
                word = porter.stem(w)
                filtered_content.append(word)

        return filtered_content

# print('kartik')

# current_dir = dirname(__file__)
# checker = PlagiarismChecker(
#     join(current_dir, "../docs/document_a.txt"),
#     join(current_dir, "../docs/document_b.txt")
# )

# print('The percentage of plagiarism held by both documents is  {0}%'.format(
#     checker.get_rate()))




class rolling_hash:
    def __init__(self, text, patternSize):
        self.text = text
        self.patternSize = patternSize
        self.base = 26
        self.window_start = 0
        self.window_end = 0
        self.mod = 5807
        self.primes = (23,209,3007,40007,500007,6000007,70000007,800007,97,100007,10017,127,10000037,1407,10057)
        self.hash = self.get_hash(text, patternSize)

    def get_hash(self, text, patternSize):
        hash_value = 0
        for i in range(0, patternSize):
            # temp = (ord(self.text[i]) - 96)*(self.base*(patternSize - i - 1))% self.mod
            # temp=(temp) % self.mod
            # hash_value = (hash_value + (temp) )% self.mod
            hash_value = (
                hash_value  * math.pow(77,i) + (self.primes[i]*  (ord(self.text[i]) - 96)*(self.base**(patternSize - i - 1)))) % self.mod
            # hash_value = (
                # hash_value + math.pow(7,i) * self.primes[i]* (ord(self.text[i]) - 96)*(self.base**(patternSize - i - 1))) % self.mod

        self.window_start = 0
        self.window_end = patternSize

        return hash_value
    
    # def rolling_hash(self,prev,next,present_hash):
    #     next_hash=present_hash
    #     for i,prime in  enumerate(prime_nos):
    #         next_hash[i]=next_hash[i]-prev
    #         next_hash[i]=next_hash[i]/prime
    #         next_hash[i]=next_hash[i]+next*math.pow(prime,2)
    #     return next_hash

    def next_window(self):
        if self.window_end <= len(self.text) - 1:
            self.hash -= (ord(self.text[self.window_start]) -
                          96)*self.base**(self.patternSize-1)

            self.hash *= self.base
            self.hash += ord(self.text[self.window_end]) - 96
            # print(  ord(self.text[self.window_end])- 96)
            self.hash %= self.mod
            self.window_start += 1
            self.window_end += 1
            return True
        return False

    def current_window_text(self):
        return self.text[self.window_start:self.window_end]


def checker(text, pattern):
    if text == "" or pattern == "":
        return None
    if len(pattern) > len(pattern):
        return None

    text_rolling = rolling_hash(text.lower(), len(pattern))
    pattern_rolling = rolling_hash(pattern.lower(), len(pattern))

    for _ in range(len(text)-len(pattern)+1):
        # print(pattern_rolling.hash, text_rolling.hash)
        if text_rolling.hash == pattern_rolling.hash:
            return "Found"
        text_rolling.next_window()
    return "Not Found"


# if __name__ == "__main__":
    # print(checker("ABDCCEAGmsslslsosspps", "agkalallaa"))
    
# text1 = "Kartik Vyas studies at IITJ"
# text2 = "Kartik Vyas is an Undergrad student at IITJ"
    
def create_rabin_karp_2_features(df): 
    rabin_karp_2_values = []

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
            object = PlagiarismChecker(answer_text,source_text)
            value = object.get_rate()
            rabin_karp_2_values.append(value)
        else:
            rabin_karp_2_values.append(-1)

    print('rabin_karp_2 features created!')
    return rabin_karp_2_values

def similarity_individual(text1,text2) :
    object = PlagiarismChecker(text1,text2)
    value = object.get_rate()
    return value

# checker = PlagiarismChecker(text1,text2)

# print('The percentage of plagiarism held by both documents is  {0}%'.format(
#     checker.get_rate()))