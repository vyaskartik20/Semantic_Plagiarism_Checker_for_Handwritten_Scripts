import os
from codes.online_real_plag import similarity
from codes.online_real_plag import individual
from codes.online_real_plag import websearch

def main():
    
    files = os.listdir('docs')
    
    for file in files :
        fileName = 'docs/' + file
        text = open(fileName, errors='ignore').read() 

        matches = similarity.report(str(text))
    
        print(f"Current File is   ::    {file}")
    
        for match in matches:
            source_text = websearch.extractText(match)
            
            plag_score = individual.check_online(text,source_text)
            
            if(plag_score > 1) :
                plag_score =1
            if(plag_score < 0) :
                plag_score = 0
            
            print(f" Plag with  {match} is   ::     {100*plag_score} ")

        print()
        print()

def web_real_online_similarity(text) : 
    matches = similarity.report(str(text))
    
    # print(f"Current File is   ::    {file}")

    data = []

    for match in matches:
        source_text = websearch.extractText(match)
        
        plag_score = individual.check_online(text,source_text)
        
        if(plag_score > 1) :
            plag_score =1
        if(plag_score < 0) :
            plag_score = 0
        
        # print(f" Plag with  {match} is   ::     {100*plag_score} ")

        temp = str({match}) + str({100 * plag_score})
        data.append( str(temp))

    return data
            # print (similarity.returnTable(similarity.report(str(file1_data))))


    # file1 = 'docs_backup/1.txt' 
    # text = open(file1, errors='ignore').read() 
    # matches = similarity.report(str(text))
    
    # for match in matches:
    #     source_text = websearch.extractText(match)
        
    #     plag_score = individual.check_online(text,source_text)
        
    #     print(f" Plag with  {match} is   ::     {plag_score} ")
        
    #     print()
    #     print()        
        # print()

    

if __name__ == '__main__':
    main()