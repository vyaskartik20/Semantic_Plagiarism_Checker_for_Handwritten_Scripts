from codes.semantic.sick_dataset_Experiment_Final.source_pytorch import individual as individualSemantic 
from codes.semantic.sick_dataset_Experiment_Final.source_pytorch.model import *

# import individual as individualSemantic
# from model import *

# text1 = "karti vyas is a boy"
# text2 = "kartik vyas is not a girl"

f = open("textfile1.txt", "r")
text1 = f.read()

f = open("textfile2.txt", "r")
text2 = f.read()

resu = individualSemantic.web_semantic_similarity(text1, text2)

f = open("textfile3.txt", "w")
f.write(str(resu))
f.close()

# def sem_plag_check(text1,text2):
#     resu = individualSemantic.web_semantic_similarity(text1, text2)
#     return(resu)