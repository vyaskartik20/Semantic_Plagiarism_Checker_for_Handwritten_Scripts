import os
import csv
import pandas as pd
import io


def dataHandler():
    filename = 'sts_train.csv'
    file_directory='dataNew/'
    df = pd.read_csv(filename)

    text=[]
    
    labels, sentence1, sentence2 = [], [], []
    
    file1=io.open("file_information.txt","w", encoding="utf-8")
    
    temp = "File" + "," + "Class" + "," + "DataType" + "Text"
    file1.write(temp)
    file1.write("\n")
    
    lengthExist = len(labels)
    
    labels = df['Class']
    sentence1 = df['Text']
    sentence2 = df['Source']
    
    i=1
    
    for j in range(0, len(labels)) :
        
        print(i)
        
        if('main' in str(labels[j])) :
            continue
        
        if('main' in str(sentence1[j])) :
            continue
        
        if('main' in str(sentence2[j])) :
            continue
        
        if(',' in str(labels[j])):
            continue
        
        if(',' in str(sentence1[j])):
            continue
        
        if(',' in str(sentence2[j])):
            continue
        
        
        # print(labels[i])
        # print(sentence1[i])
        # print(sentence2[i])
        
        file1Name = "source" + str(i) + ".txt"
        file2Name = "answer" + str(i) + ".txt"
        
        a = file1Name + "," + str(-1) + "," + str("orig") + "," + str(sentence2[j])
        datatype = "train" 
        b = file2Name + "," + str(labels[j]) + "," + str(datatype) + "," + str(sentence1[j])

        file3=io.open(file1Name,"w",encoding="utf-8")
        file3.write(str(sentence2[j]))
        file3.close()
        
        file2=io.open(file2Name,"w", encoding="utf-8")
        file2.write(str(sentence1[j]))
        file2.close()

        a = str(a)
        b = str(b)
        
        # with io.open(fname, "w", ) as f:

        
        file1.write(a)
        file1.write("\n")
        file1.write(b)
        file1.write("\n")
        
        i = i+1
        
        
    filename = 'sts_test.csv'
    file_directory='dataNew/'
    df = pd.read_csv(filename)

    text=[]
    
    labels, sentence1, sentence2 = [], [], []
    
    # file1=open("file_information2.txt","w")
    
    labels = df['Class']
    sentence1 = df['Text']
    sentence2 = df['Source']
    
    # i=lengthExist
    
    for j in range(lengthExist, (lengthExist + len(labels))) :
        print(i)
        
        if('main' in str(labels[j])) :
            continue
        
        if('main' in str(sentence1[j])) :
            continue
        
        if('main' in str(sentence2[j])) :
            continue
        
        if(',' in str(labels[j])):
            continue
        
        if(',' in str(sentence1[j])):
            continue
        
        if(',' in str(sentence2[j])):
            continue
        
        file1Name = "source" + str(i) + ".txt"
        file2Name = "answer" + str(i) + ".txt"
        
        a = file1Name + "," + str(-1) + "," + str("orig") + "," + str(sentence2[j])
        datatype = "train" 
        b = file2Name + "," + str(labels[j]) + "," + str(datatype) + "," + str(sentence1[j])

        file3=io.open(file1Name,"w", encoding="utf-8")
        file3.write(str(sentence2[j]))
        file3.close()
        
        file2=io.open(file2Name,"w", encoding="utf-8")
        file2.write(str(sentence1[j]))
        file2.close()

        a = str(a)
        b = str(b)
        
        file1.write(a)
        file1.write("\n")
        file1.write(b)
        file1.write("\n")
        i= i+1
        
    file1.close()

# def dataLoader(filename):
#     """
#     The corpus contains lots of things which are not of our interest.
#     Read file and discard things that are of not interest to us.
#     :param filename:
#     :return: sentencesX, sentencesY, label
#     :return type: list of sentence, list of sentence, list of bools
#     :param sentence type : string
#     """
#     if not os.path.exists(filename):
#         raise ValueError("{} file does not exist.")

#     # Read file and split into lines
#     text = open(filename, mode='r', encoding='utf8').read().lower().splitlines()

#     labels, sentence1, sentence2 = [], [], []
#     i=1
    
#     # with open('file_information.txt', 'w') as csvfile:
#     #         filewriter0 = csv.writer(csvfile, delimiter=',',
#     #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     # filewriter0.writerow(['File', 'Class'])
    
#     file1=open("file_information.txt","w")
    
#     temp = "File" + "," + "Class" + "," + "DataType"
#     file1.write(temp)
#     file1.write("\n")
      
#     for line in text[1:]:
#         _, s1, s2, _ ,label, _ , _ , _ , _ , _ , _ , datatype = line.split("\t")

#         labels.append(label)
#         sentence1.append(s1)
#         sentence2.append(s2)
        
#         file1Name = "dataNew/source" + str(i) + ".txt"
#         file2Name = "dataNew/answer" + str(i) + ".txt"
       
#         i=i+1
        
#         # file3=open(file1Name,"w")
#         # file3.write(s1)
#         # file3.close()
        
#         # file2=open(file2Name,"w")
#         # file2.write(s2)
#         # file2.close()
        
#         a = file1Name + "," + str(-1) + "," + str("orig")
#         if(datatype == "trial") :
#             datatype = "train" 
#         b = file2Name + "," + str(label) + "," + str(datatype) 

#         a = str(a)
#         b = str(b)
        
#         file1.write(a)
#         file1.write("\n")
#         file1.write(b)
#         file1.write("\n")
        
        
#     file1.close()

#     # labels = list(map(int, labels))

#     # return labels, sentence1, sentence2




if __name__ == '__main__':
    # filename = "SICK.txt"
    # dataLoader(filename)
    # print(label[0], sx[0], sy[0])
    
    # dataHandler()

    read_file = pd.read_csv (r'file_information.txt')
    read_file.columns = ['File','Class', 'Datatype', 'Text']
    read_file.to_csv (r'data/file_information.csv', index=None)
    