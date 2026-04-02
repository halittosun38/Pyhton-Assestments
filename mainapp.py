from tkinter import *
from tkmacosx import *
from tkinter import messagebox

root = Tk()
root.title("Assestment App")
root.geometry("720x1280")

label1 = Label(root, text="Test")
label1.pack()

entry1 = Entry(root)
entry1.pack()


def student_exists(data):
    try:
        with open("data.txt", "r") as file:
            content = file.read().split("|")
            return data in content
    except FileNotFoundError:
        return False


def adddata(data):
    if student_exists(data):
        messagebox.showerror("Error", "Student number already exists!")
        return False
    else:
        with open("data.txt", "a") as file: 
            file.write(str(data) + "|")
        return True


def createpopup1():
    root.attributes('-alpha', 0.6)

    pop = Toplevel(root)
    pop.geometry("300x200")
    pop.config(bg="#444444", highlightbackground="#FFFFFF", highlightthickness=2)
    pop.grab_set()
    label3 = Label(pop,text="Add New Student",background="#444444")
    label3.pack()
    label4 = Label(pop,text="",background="#444444",font="Arrial")
    label4.pack()
    label2 = Label(pop, text="Student No",background="#444444")
    label2.pack()

    entry2 = Entry(pop)
    entry2.pack()

    def closepopup1():
        root.attributes('-alpha', 1)
        pop.destroy()

    def save():
        if adddata(entry2.get()):
            closepopup1()

    button_save = Button(pop, text="Save", command=save)
    button_save.pack(pady=5)

    button_cancel = Button(pop, text="Cancel", command=closepopup1)
    button_cancel.pack(pady=5)


button1 = Button(root, command=createpopup1, text="Button For blur")
button1.pack(padx=20, pady=20)

root.mainloop()