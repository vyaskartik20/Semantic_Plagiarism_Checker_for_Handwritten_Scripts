from sklearn.feature_extraction.text import CountVectorizer
# Should return a list of length 100 for all files in a complete_df

def calculate_containment_individual(text1,text2 , n):
    counts = CountVectorizer(analyzer='word', ngram_range=(n,n))
    ngrams = counts.fit_transform([text1, text2])
    ngram_array = ngrams.toarray()

    intersection = [min(a, s) for a, s in zip(*ngram_array)]
    c_value = sum(intersection) / sum(ngram_array[0])

    return c_value

# Calculate the ngram containment for one answer file/source file pair in a df
def calculate_containment(df, n, answer_filename):
    """
    Calculates the containment between a given answer text and its associated source text.
    This function creates a count of ngrams (of a size, n) for each text file in our data.
    Then calculates the containment by finding the ngram count for a given answer text, 
    and its associated source text, and calculating the normalized intersection of those counts.
    
    Arguments
    :param df: A dataframe with columns,
        'File', 'Task', 'Category', 'Class', 'Text', and 'Datatype'
    :param n: An integer that defines the ngram size
    :param answer_filename: A filename for an answer text in the df, ex. 'g0pB_taskd.txt'
    
    Return
    :return: A single containment value that represents the similarity
        between an answer text and its source text.
    """
    
    answer_df = df.query('File == @answer_filename')
    a_text = answer_df.iloc[0].at['Text']
    # source_filename = answer_filename
    # source_filename[0]="s"
    # source_filename[1]="o"
    # source_filename[2]="u"
    # source_filename[3]="r"
    # source_filename[4]="c"
    # source_filename[5]="e"
    source_filename = "source" + answer_filename[6:]
    source_df = df.query('File == @source_filename')
    s_text = source_df.iloc[0].at['Text']

    counts = CountVectorizer(analyzer='word', ngram_range=(n,n))
    ngrams = counts.fit_transform([a_text, s_text])
    ngram_array = ngrams.toarray()

    intersection = [min(a, s) for a, s in zip(*ngram_array)]
    c_value = sum(intersection) / sum(ngram_array[0])

    return c_value


def create_containment_features(df, n, column_name=None):
    
    containment_values = []
    
    if(column_name==None):
        column_name = 'c_'+str(n) # c_1, c_2, .. c_n
    
    # iterates through dataframe rows
    for i in df.index:
        file = df.loc[i, 'File']
        # Computes features using calculate_containment function
        if df.loc[i,'Class'] > -1:
            c = calculate_containment(df, n, file)
            containment_values.append(c)
        # Sets value to -1 for original tasks 
        else:
            containment_values.append(-1)
    
    print(str(n)+'-gram containment features created!')
    return containment_values