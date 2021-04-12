# import os
# import torch
# from torch import Tensor
from model import *

import individual as individualSemantic 
text1 = "karti vyas is a boy"
text2 = "kartik vyas is not a girl"

resu = individualSemantic.web_semantic_similarity(text1, text2)
print(resu)
