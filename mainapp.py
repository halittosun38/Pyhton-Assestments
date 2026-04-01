from tkinter import *
from tkmacosx import *
root = Tk()
root.title("Assestment App")
root.geometry("720x1280")
label1=Label(root,text="Test")
label1.pack()
entry1 = Entry(root)
entry1.pack()


def adddata(data):
    with open("data.txt", "w") as files:
        files.write(str(data)+" |")

def createpopup():
    root.attributes('-alpha',0.6)
    
button1 = Button(root,command=createpopup,text="Button For blur")
button1.pack(padx=20, pady=20)
root.mainloop()

