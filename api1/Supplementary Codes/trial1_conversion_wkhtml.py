import os
import pdfkit
 
# convert txt into pdf
# https://wkhtmltopdf.org/ 
 
pdfkit.from_file("OUTPUT.txt", "text_pdf.pdf")
 
os.startfile("text_pdf.pdf")