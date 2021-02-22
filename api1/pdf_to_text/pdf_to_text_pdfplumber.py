import pdfplumber
import os

for file in os.listdir('docs_pdf') : 
    fileName = 'docs/' + file
    with pdfplumber.open(r'fileName') as pdf:
        number_of_pages = len(pdf.pages)
        print(number_of_pages)
        
        fileName2 = file.split('.')
        
        outputFile = 'outputTXT/' + fileName2[0] + '.txt' 
        file1 = open(outputFile, 'w')
        for i in range(0, number_of_pages):
            page = pdf.pages[i]
            print(i)
            print(page.extract_text())
            file1.write(page.extract_text())
            file1.write("\n")
        file1.close()
