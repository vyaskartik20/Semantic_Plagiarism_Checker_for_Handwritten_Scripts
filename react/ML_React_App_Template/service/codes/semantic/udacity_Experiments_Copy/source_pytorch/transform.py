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
            # filewriter0 = csv.writer(csvfile, delimiter=',',
                            # quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # filewriter.writerow(['File', 'Class'])
    
    file1=open("file_information.txt","w")
    
    temp = "File" + "," + "Class"
    file1.write(temp)
    file1.write("\n")
      
    for line in text[1:]:
        label, _, _, s1, s2 = line.split("\t")

        labels.append(label)
        sentence1.append(s1)
        sentence2.append(s2)
        
        file1Name = "source" + str(i) + ".txt"
        file2Name = "answer" + str(i) + ".txt"
       
        i=i+1
        
        # file1=open(file1Name,"w")
        # file1.write(s1)
        # file1.close()
        
        # file2=open(file2Name,"w")
        # file2.write(s2)
        # file2.close()
        
        a = file1Name + "," + str(-1) 
        b = file2Name + "," + str(label) 

        a = str(a)
        b = str(b)
        
        file1.write(a)
        file1.write("\n")
        file1.write(b)
        file1.write("\n")
        
        
    file1.close()

    labels = list(map(int, labels))

    return labels, sentence1, sentence2


if __name__ == '__main__':
    filename = "msr_paraphrase_train.txt"
    label, sx, sy = dataLoader(filename)
    print(label[0], sx[0], sy[0])
    