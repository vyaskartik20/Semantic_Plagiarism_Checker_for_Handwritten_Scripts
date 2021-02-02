import os
import csv

def dataLoader(filename):
    """
    The corpus contains lots of things which are not of our interest.
    Read file and discard things that are of not interest to us.
    :param filename:
    :return: sentencesX, sentencesY, label
    :return type: list of sentence, list of sentence, list of bools
    :param sentence type : string
    """
    if not os.path.exists(filename):
        raise ValueError("{} file does not exist.")

    # Read file and split into lines
    text = open(filename, mode='r', encoding='utf8').read().lower().splitlines()

    labels, sentence1, sentence2 = [], [], []
    i=1
    
    # with open('file_information.txt', 'w') as csvfile:
    #         filewriter0 = csv.writer(csvfile, delimiter=',',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # filewriter0.writerow(['File', 'Class'])
    
    file1=open("file_information.txt","w")
    
    temp = "File" + "," + "Class" + "," + "DataType"
    file1.write(temp)
    file1.write("\n")
      
    for line in text[1:]:
        _, s1, s2, _ ,label, _ , _ , _ , _ , _ , _ , datatype = line.split("\t")

        labels.append(label)
        sentence1.append(s1)
        sentence2.append(s2)
        
        file1Name = "source" + str(i) + ".txt"
        file2Name = "answer" + str(i) + ".txt"
       
        i=i+1
        
        # file3=open(file1Name,"w")
        # file3.write(s1)
        # file3.close()
        
        # file2=open(file2Name,"w")
        # file2.write(s2)
        # file2.close()
        
        a = file1Name + "," + str(-1) + "," + str("orig")
        if(datatype == "trial") :
            datatype = "train" 
        b = file2Name + "," + str(label) + "," + str(datatype) 

        a = str(a)
        b = str(b)
        
        file1.write(a)
        file1.write("\n")
        file1.write(b)
        file1.write("\n")
        
        
    file1.close()

    # labels = list(map(int, labels))

    # return labels, sentence1, sentence2


import pandas as pd

if __name__ == '__main__':
    # filename = "SICK.txt"
    # dataLoader(filename)
    # print(label[0], sx[0], sy[0])
    

    read_file = pd.read_csv (r'file_information.txt')
    read_file.columns = ['File','Class', 'Datatype']
    read_file.to_csv (r'data/file_information.csv', index=None)
    