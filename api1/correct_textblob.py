from textblob import TextBlob

file1 = open("inputFinal.txt","r+")
a=file1.read();

print("Original text : " + str(a))

b=TextBlob(a)

print("Corrected Text : " + str(b.correct()) )

file1.close()

file2=open("outputFinal1.txt","w")
file2.write(str(b.correct()))
file2.close()