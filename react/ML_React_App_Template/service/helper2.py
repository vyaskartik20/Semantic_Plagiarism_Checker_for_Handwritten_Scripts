from codes.semantic.sick_dataset_Experiment_Final.source_pytorch_entailment import individual as individualEntailment

# text1 = "kartik vyas is a boy"
# text2 = "kartik vyas is not a girl"

def entailment_check(text1,text2):
    resu = individualEntailment.web_entailment_analysis(text1, text2)
    return(resu)