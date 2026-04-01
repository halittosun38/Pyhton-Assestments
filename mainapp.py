from tkinter import *
from tkmacosx import *
from tkinter import messagebox
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

def createpopup1():

    root.attributes('-alpha',0.6)
    pop = Toplevel(root)
    pop.geometry("300x200")
    pop.config(bg="white", highlightbackground="#000000", highlightthickness=2)
    def closepopup1():
        root.attributes('-alpha',1)
        pop.destroy()
    button2 = Button(pop,command=closepopup1,text="sss")
    button2.pack()

    
button1 = Button(root,command=createpopup1,text="Button For blur")
button1.pack(padx=20, pady=20)
root.mainloop()

