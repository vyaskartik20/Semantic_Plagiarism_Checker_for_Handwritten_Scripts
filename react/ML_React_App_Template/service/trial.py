# from flask import Flask
from codes.online_real_plag import main

data= "apj abdul kalam president of the INida"
# data2= "Kartik teaches at IIT Jodhpur"

file1 = 'codes/online_real_plag/docs_backup/' + '1.txt'
text1 = open(file1, errors='ignore').read()

data = main.web_real_online_similarity(text1)

data = [val for val in data]

for val in data :
    print(val)
    # point = [va for va in val]
    # print
    # for point in val :
        # print(point)
    # print( str(point[0]) + str(" : ") + str(point[1]) )


# print(data)