from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

subscription_key = "9091fe4cca97412981ea68f2da36ba32"
endpoint = "https://textconversion.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

print("===== Batch Read File - local =====")
# D:\BTP-2\api1\imag\1608557373
local_image_handwritten_path = "D:\BTP-2\\api1\\imag\\1609349852\\output13.jpg"
local_image_handwritten = open(local_image_handwritten_path, "rb")

recognize_handwriting_results = computervision_client.read_in_stream(local_image_handwritten, raw=True)
operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
operation_id_local = operation_location_local.split("/")[-1]

while True:
    recognize_handwriting_result = computervision_client.get_read_result(operation_id_local)
    if recognize_handwriting_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

file2=open("inputFinal.txt","w")
if recognize_handwriting_result.status == OperationStatusCodes.succeeded:
    for text_result in recognize_handwriting_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            file2.write(str(line.text))
            
print()
file2.close()




















# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials

# from array import array
# import os
# from PIL import Image
# import sys
# import time

# subscription_key = "9091fe4cca97412981ea68f2da36ba32"
# endpoint = "https://textconversion.cognitiveservices.azure.com/"

# computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


# '''
# Batch Read File, recognize handwritten text - local
# This example extracts text from a handwritten local image, then prints results.
# This API call can also recognize remote image text (shown in next example, Batch Read File - remote).
# '''
# print("===== Batch Read File - local =====")
# # Get image of handwriting
# # D:\BTP-2\api1\imag\1608557373
# local_image_handwritten_path = "D:\BTP-2\\api1\\imag\\1608726197\output13.jpg"
# # Open the image
# local_image_handwritten = open(local_image_handwritten_path, "rb")

# # Call API with image and raw response (allows you to get the operation location)
# recognize_handwriting_results = computervision_client.read_in_stream(local_image_handwritten, raw=True)
# # Get the operation location (URL with ID as last appendage)
# operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
# # Take the ID off and use to get results
# operation_id_local = operation_location_local.split("/")[-1]

# # Call the "GET" API and wait for the retrieval of the results
# while True:
#     recognize_handwriting_result = computervision_client.get_read_result(operation_id_local)
#     if recognize_handwriting_result.status not in ['notStarted', 'running']:
#         break
#     time.sleep(1)

# # Print results, line by line
# file2=open("inputFinal.txt","w")
# if recognize_handwriting_result.status == OperationStatusCodes.succeeded:
#     for text_result in recognize_handwriting_result.analyze_result.read_results:
#         for line in text_result.lines:
#             print(line.text)
#             file2.write(str(line.text))
#             # print(line.bounding_box)
            
# print()
# file2.close()