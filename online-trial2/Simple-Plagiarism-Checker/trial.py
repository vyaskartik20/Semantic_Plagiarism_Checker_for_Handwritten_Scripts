import re
import math

universalSetOfUniqueWords = []
matchPercentage = 0

inputQuery = 'Avul Pakir Jainulabdeen Abdul Kalam (/ˈæbdəl kəˈlɑːm/ (About this soundlisten); 15 October 1931 – 27 July 2015) was an Indian aerospace scientist and politician who served as the 11th President of India from 2002 to 2007. He was born and raised in Rameswaram, Tamil Nadu and studied physics and aerospace engineering. He spent the next four decades as a scientist and science administrator, mainly at the Defence Research and Development Organisation (DRDO) and Indian Space Research Organisation (ISRO) and was intimately involved in India .[1] He thus came to be known as the Missile Man of India for his work on the development of ballistic missile and launch vehicle technology.[2][3][4] He also played a pivotal organisational, technical, and political role in Indias Pokhran-II nuclear tests in 1998, the first since the original nuclear test by India in 1974.[5] Kalam was elected as the 11th President of India in 2002 with the support of both the ruling Bharatiya Janata Party and the then-opposition Indian National Congress. Widely referred to as the "Peoples President",[6] he returned to his civilian life of education, writing and public service after a single term. He was a recipient of several prestigious awards, including the Bharat Ratna, Indias highest civilian honour. While delivering a lecture at the Indian Institute of Management Shillong, Kalam collapsed and died from an apparent cardiac arrest on 27 July 2015, aged 83.[7] Thousands, including national-level dignitaries, attended the funeral ceremony held in his hometown of Rameswaram, where he was buried with full state honours.[8]'

lowercaseQuery = inputQuery.lower()

queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()			#Replace punctuation by space and split
# queryWordList = map(str, queryWordList)					#This was causing divide by zero error

for word in queryWordList:
    if word not in universalSetOfUniqueWords:
        universalSetOfUniqueWords.append(word)

fd = open("database1.txt", "r")
database1 = fd.read().lower()

databaseWordList = re.sub("[^\w]", " ",database1).split()	#Replace punctuation by space and split
# databaseWordList = map(str, databaseWordList)			#And this also leads to divide by zero error

for word in databaseWordList:
    if word not in universalSetOfUniqueWords:
        universalSetOfUniqueWords.append(word)

queryTF = []
databaseTF = []

for word in universalSetOfUniqueWords:
    queryTfCounter = 0
    databaseTfCounter = 0

    for word2 in queryWordList:
        if word == word2:
            queryTfCounter += 1
    queryTF.append(queryTfCounter)

    for word2 in databaseWordList:
        if word == word2:
            databaseTfCounter += 1
    databaseTF.append(databaseTfCounter)

dotProduct = 0
for i in range (len(queryTF)):
    dotProduct += queryTF[i]*databaseTF[i]

queryVectorMagnitude = 0
for i in range (len(queryTF)):
    queryVectorMagnitude += queryTF[i]**2
queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

databaseVectorMagnitude = 0
for i in range (len(databaseTF)):
    databaseVectorMagnitude += databaseTF[i]**2
databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude))*100

'''
print queryWordList
print
print databaseWordList


print queryTF
print
print databaseTF
'''

output = "Input query text matches %0.02f%% with database."%matchPercentage
print(output)
