# importing required modules
import PyPDF2

# creating a pdf file object
pdfFileObj = open('B18CSE002_tut3.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(4)

# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()
