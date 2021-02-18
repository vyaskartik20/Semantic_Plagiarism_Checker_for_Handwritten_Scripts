import numpy as np

def lcs_norm_word(answer_text, source_text):
    """
    Computes the longest common subsequence of words in two texts;
    returns a normalized value.
    
    Arguments:
    :param answer_text: The pre-processed text for an answer text
    :param source_text: The pre-processed text for an answer's associated source text
    
    Return:
    :return: A normalized LCS value
    """

    answer_words = answer_text.split()
    answer_len = len(answer_words)
    source_words = source_text.split()
    source_len = len(source_words)

    lcs_matrix = np.zeros(shape=(source_len+1,answer_len+1), dtype='int')

    for i, s in enumerate(source_words, 1):
        for j, a in enumerate(answer_words, 1):
            if a == s:
                lcs_matrix[i,j] = lcs_matrix[i-1,j-1] + 1
            else:
                lcs_matrix[i,j] = max(lcs_matrix[i,j-1], lcs_matrix[i-1,j])

    return lcs_matrix[source_len][answer_len] / answer_len


# Function creates lcs feature and add it to the dataframe
def create_lcs_features(df, column_name='lcs_word'):
    
    lcs_values = []
    
    # iterate through files in dataframe
    for i in df.index:
        # Computes LCS_norm words feature using function above for answer tasks
        if df.loc[i,'Class'] != -1:
            # get texts to compare
            answer_text = df.loc[i, 'Text']
            answer_filename = df.loc[i, 'File'] 
            # task = df.loc[i, 'Task']
            # we know that source texts have Class = -1
            # orig_rows = df[(df['Class'] == -1)]
            # orig_row = orig_rows[(orig_rows['Task'] == task)]
            # source_text = orig_row['Text'].values[0]
            source_filename = answer_filename
            # source_filename[0]='s'
            # source_filename[1]='o'
            # source_filename[2]='u'
            # source_filename[3]='r'
            # source_filename[4]='c'
            # source_filename[5]='e'
            source_filename = "source" + answer_filename[6:]     
            source_df = df.query('File == @source_filename')
            source_text = source_df.iloc[0].at['Text']

            # calculate lcs
            lcs = lcs_norm_word(answer_text, source_text)
            lcs_values.append(lcs)
        # Sets to -1 for original tasks 
        else:
            lcs_values.append(-1)

    print('LCS features created!')
    return lcs_values