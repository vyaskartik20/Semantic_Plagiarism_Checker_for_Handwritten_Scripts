import pdfplumber
with pdfplumber.open(r'B18CSE002_tut3.pdf') as pdf:
    number_of_pages = len(pdf.pages)
    print(number_of_pages)
    file1 = open('test.txt', 'w')
    for i in range(0, number_of_pages):
        page = pdf.pages[i]
        print(i)
        print(page.extract_text())
        file1.write(page.extract_text())
        file1.write("\n")
    file1.close()
