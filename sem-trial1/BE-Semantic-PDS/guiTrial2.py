from tkinter import *
import os
from finalSimilarity2 import *

def clearAll():
    res.delete(0, END)
    para_res.delete(0, END)
    sem_res.delete(0, END)
    txt.delete(0, END)

def input_txt():
   with open("input.txt", 'wb') as outfile:
       outfile.write(txt.get().encode("utf-8"))
   os.system('python instance.py')
   CS = lsa()
   DS = doc_sim()
   sem_res.insert(10, str(CS))
   res.insert(10, str(DS))
   paraVal = paraphrase()
   if paraVal == 0:
       para_res.insert(10, "NO")
   else:
       para_res.insert(10, "YES")

window = Tk()
window.title("Plagiarism Check")
window.geometry('600x400')

heading = Label(window, text="Welcome to PlagiarX", font=("Arial Bold", 30), fg="blue")
heading.place(relx=0.5, x=-6, y=40, anchor=CENTER)

text = Label(window, text="Enter text")
text.place(relx=0, x=30, y=80, anchor=NW)

btn = Button(window, text="Check", command=input_txt)
txt = Entry(window, width = 60)

txt.place(relx=0, x=50, y=120, anchor=NW, height=50)
btn.place(relx=0.5, rely=0.5, anchor=CENTER)

semantic_sim = Label(window, text="Semantic Similarity : ", fg="black")
semantic_sim.place(relx=0, x=30, y=220, anchor=NW)
sem_res = Entry(window)
sem_res.place(relx=0.5, x=-120, y=220, anchor=NW)

parap = Label(window, text="Paraphrase : ", fg="black")
parap.place(relx=0, x=30, y=270, anchor=NW)
para_res = Entry(window)
para_res.place(relx=0.5, x=-120, y=270, anchor=NW)

plag_result = Label(window, text="Plagiarism % : ", fg="red")
plag_result.place(relx=0, x=30, y=320, anchor=NW)
res = Entry(window)
res.place(relx=0.5, x=-120, y=320, anchor=NW)

clearAllEntry = Button(window, text = "Clear All", fg = "Black", bg = "Red", command = clearAll)
clearAllEntry.place(relx=0.5, rely=0.95, anchor=CENTER)

window.mainloop()



