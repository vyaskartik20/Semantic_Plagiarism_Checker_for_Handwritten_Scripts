from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
import os
import sys
import time
import gc

outputDir = "imag/"

def convert(file, outputDir):
    outputDir = outputDir + str(round(time.time())) + '/'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)


    info = pdfinfo_from_path(file, userpw=None, poppler_path=None)

    maxPages = info["Pages"]
    counter = 1
    for page in range(1, maxPages+1, 10) : 
        pages = convert_from_path(file, dpi=200, first_page=page, last_page = min(page+10-1,maxPages))
        for page in pages:
            myfile = outputDir +'output' + str(counter) +'.jpg'
            counter = counter + 1
            page.save(myfile, "JPEG")
            print(myfile)
        gc.collect()


    # pages = convert_from_path(file, 500)


args = sys.argv
if len(args) > 1:
    file = args[1]
    convert(file, outputDir)