from spellchecker import SpellChecker

spell = SpellChecker()

filePath="D:\BTP-2\\api1\\inputFinal.txt"

f = open(filePath).read()

file2=open("outputPySpellChecker.txt","w")

for word in f.split():
    # do something with word
    print (word + '   ' + spell.correction(word) )
    file2.write(spell.correction(word))
    file2.write(' ')
  
file2.close()