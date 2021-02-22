from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import pkg_resources
from symspellpy import SymSpell, Verbosity
from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
import gc
from array import array
import os
from PIL import Image
import sys
import time

outputDir = "imag/"

def convert(file, outputDir):
    outputDir = outputDir + '/'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)


    info = pdfinfo_from_path(file, userpw=None, poppler_path=None)

    maxPages = info["Pages"]
    counter = 1
    # print("Images extracted from pdf : ")
    for page in range(1, maxPages+1, 10) : 
        pages = convert_from_path(file, dpi=200, first_page=page, last_page = min(page+10-1,maxPages))
        for page in pages:
            myfile = outputDir +'output' + str(counter) +'.jpg'
            counter = counter + 1
            page.save(myfile, "JPEG")
            # print(myfile)
        gc.collect()
    print("PDF to images conversion completed")
    print()

    # pages = convert_from_path(file, 500)

if  __name__ == '__main__' :
    args = sys.argv
    if len(args) > 1:
        file = args[1]
        # convert(file, outputDir)
        
        
        
        subscription_key = "9091fe4cca97412981ea68f2da36ba32"
        endpoint = "https://textconversion.cognitiveservices.azure.com/"

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        print("Processing images for conversion to text")
        
        file2=open("inputFinal.txt","w")
        folderName = "D:\\BTP-2\\api1\\imag\\"
        fileNames = os.listdir(folderName)
        i=0
        while True :
            try :
                print(fileNames[i])
                # local_image_handwritten_path = "D:\BTP-2\\api1\\imag\\1609349852\\output13.jpg"
                local_image_handwritten_path = "D:\\BTP-2\\api1\\imag\\" + str(fileNames[i])
                # print(fileName)
                local_image_handwritten = open(local_image_handwritten_path, "rb")

                recognize_handwriting_results = computervision_client.read_in_stream(local_image_handwritten, raw=True)
                operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
                operation_id_local = operation_location_local.split("/")[-1]

                while True:
                    recognize_handwriting_result = computervision_client.get_read_result(operation_id_local)
                    if recognize_handwriting_result.status not in ['notStarted', 'running']:
                        break
                    time.sleep(1)

                if recognize_handwriting_result.status == OperationStatusCodes.succeeded:
                    for text_result in recognize_handwriting_result.analyze_result.read_results:
                        for line in text_result.lines:
                            # print(line.text)
                            file2.write(str(line.text))
                i = i+1
                
                if i >= len(fileNames) :
                    break
            except :
                # i = i-2
                print('waiting to reinitiate')
                time.sleep(60)        
        print('Finished and text saved')
        print()
        file2.close()
        
        
        
        
        print('Improving Conversion Accuracy')
        
        
        sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
        
        
        filePath="D:\BTP-2\\api1\\inputFinal.txt"
        f = open(filePath).read()
        file2=open("inputFinal2.txt","w")
        
        splittingAgents= ['.' , '?' , '(' , ')' , ':' , ',' , '[' , ']' , '/' , '|' , '{' , '}' , '+' , ':' ,  '"' , ';' , '<' , '>']
        spaceAgents =  ['?' , ')' , ':' , ',' , ']' , '/' , '|' , '}' , '-' , '+' , ':' , ';' , '<' , '>']

        phrase=""

        for c in f : 
            if c in splittingAgents:
                input_term = phrase
                # max edit distance per lookup (per single word, not per whole input string)
                suggestions = sym_spell.lookup_compound(input_term, max_edit_distance=2)
                # display suggestion term, edit distance, and term frequency
                for suggestion in suggestions:
                    # for part in suggestion:
                    part = str(suggestion.term)
                    # print(part)
                    file2.write(part)
                    file2.write(c)
                    if c in spaceAgents :
                        file2.write(' ')
                phrase = ""
            else : 
                phrase = phrase + c
                
        input_term = phrase
        suggestions = sym_spell.lookup_compound(input_term, max_edit_distance=2)
        for suggestion in suggestions:
            part = str(suggestion.term)
            file2.write(part)
        file2.close()
        
        filePath="D:\BTP-2\\api1\\inputFinal2.txt"
        f = open(filePath).read()
        file2=open("OUTPUT.txt","w")
        
        for sentence in f.split('.'):
            sentence2 = sentence.capitalize()
            file2.write(sentence2)
            file2.write('. ')
            
        file2.close()
        
        print('ALL DONE')