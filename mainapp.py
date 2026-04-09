# source: https://docs.python.org/3/library/tkinter.html
from tkinter import *
from tkinter import messagebox, ttk

# source: https://docs.python.org/3/library/json.html
import json

# source: https://matplotlib.org/stable/tutorials/introductory/pyplot.html
import matplotlib.pyplot as plt


# Its Create Main Screen
# Tk()              -- Start to main app screen
# title()           -- Screen Name
# geometry()   -- Screen Resolation
# resizable(F, F)   -- if we use like that screen connot resizable
root = Tk()
root.title("Student Progress Tracker")
root.geometry("600x650")
root.resizable(False, False)



#source: https://stackoverflow.com/questions/20199126/reading-json-from-a-file

#######################  Json Read-Write #####################################
def load_datajsonss():
    ## this code reads the students.json file and returns it as a Python dictionary.
    ### FileNotFound = if data file did't created it gives error
    ###  JsonDecodeError = If the file is corrupted, warns the user and returns an empty dictionary
    try:
        with open("students.json", "r") as file:
            return json.load(file)       
    except FileNotFoundError:
        return {}                         
    except json.JSONDecodeError:
        messagebox.showerror("Error", "students.json is corrupted. Starting fresh.")
        return {}


def save_data(data):
   ##Writes the Python dictionary to the students.json file.
    with open("students.json", "w") as file:
        json.dump(data, file, indent=4)

## input checker

def check_student_id(student_id):
    #### Checks if the Student ID is valid.

    if not student_id.strip():
        messagebox.showerror("Checking Error", "Student ID cannot be empty.")
        return False
    if not student_id.replace("_", "").replace("-", "").isalnum():
        messagebox.showerror("Checking Error","Student ID must be alphanumeric .")
        return False
    return True


def check_grade(grade_str):

    ## source: https://docs.python.org/3/library/functions.html#float
     #####Checks if the grade input is a valid numeric value.
    try:
        grade = float(grade_str)
    except ValueError:
        messagebox.showerror("Checking Error", "Grade must be a number.")
        return None
    if not (0 <= grade <= 100):
        messagebox.showerror("Checking Error", "Grade must be between 0 and 100.")
        return None
    return grade


def check_attendance(att_str):
####Checks if the attendance percentage is valid.
    try:
        attandancs = float(att_str)
    except ValueError:
        messagebox.showerror("Checking Error", "Attendance must be a number.")
        return None
    if not (0 <= attandancs <= 100):
        messagebox.showerror("Checking Error", "Attendance must be between 0 and 100.")
        return None
    return attandancs


##### Main Functions

def add_student(student_id):
## This functions add a new student in the library
    if not check_student_id(student_id):
        return False
    data = load_datajsonss()
    if student_id in data:
        messagebox.showerror("Error", f"Student '{student_id}' already exists.")
        return False
    data[student_id] = {"grades": {}, "attendance": 0}
    save_data(data)
    return True


def delete_student(student_id):
## This codes delete a student who is written
    data = load_datajsonss()
    if student_id in data:
        del data[student_id]
        save_data(data)
        return True
    else:
        messagebox.showerror("Error", f"Student '{student_id}' not found.")
        return False


def add_grade(student_id, subject, grade_str):
### This code add a new grade
    if not check_student_id(student_id):
        return False
    if not subject.strip():
        messagebox.showerror("Validation Error", "Subject cannot be empty.")
        return False
    grade = check_grade(grade_str)
    if grade is None:
        return False
    data = load_datajsonss()
    if student_id not in data:
        messagebox.showerror("Error", f"Student '{student_id}' not found.")
        return False
    data[student_id]["grades"][subject.strip()] = grade   
    save_data(data)
    return True


def set_attendance(student_id, att_str):
### Set student attendance percent on here
    if not check_student_id(student_id):
        return False
    attandance = check_attendance(att_str)
    if attandance is None:
        return False
    data = load_datajsonss()
    if student_id not in data:
        messagebox.showerror("Error", f"Student '{student_id}' not found.")
        return False
    data[student_id]["attendance"] = attandance
    save_data(data)
    return True

#Calculating functions

def calculate_average(student_id):
    #Calculates the arithmetic mean of all grades for a specific student.
    #Uses dict.get() to safely access data and avoid KeyError.
    ## source: https://docs.python.org/3/library/stdtypes.html#dict.get
    data = load_datajsonss()
    if student_id in data:
        grades = list(data[student_id].get("grades", {}).values())
        if len(grades) == 0:
            return 0.0
        return sum(grades) / len(grades)    # Takes summ of the grades and divede
    return 0.0


def school_average():
### Calculates the overall average across all students in the school.
    data = load_datajsonss()
    averages = [calculate_average(sid) for sid in data]
    if not averages:
        return 0.0
    return sum(averages) / len(averages)


def get_letter_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


# Search And Sorting

def search_students(search_filtring_inputs):

    ## source: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    ## purpose: Comprehension sözdizimi ile filtreleme
    
    data = load_datajsonss()
    search_filtring_inputs = search_filtring_inputs.strip().lower()
    return {sid: data[sid] for sid in data if search_filtring_inputs in sid.lower()}


def sort_students(by="id", reverse=False):
  
    ## source https://medium.com/@brentwash35/lambda-functions-in-python-the-complete-guide-with-real-world-examples-1f1bab9f4964
    ## source: https://docs.python.org/3/howto/sorting.html
    #Sorts student records based on the chosen criteria (ID, average, or attendance).
    #Returns a sorted list of tuples (id, data).

    data = load_datajsonss()
    if by == "average":
        return sorted(data.items(), key=lambda x: calculate_average(x[0]), reverse=reverse)
    elif by == "attendance":
        return sorted(data.items(), key=lambda x: x[1].get("attendance", 0), reverse=reverse)
    else:
        return sorted(data.items(), key=lambda x: x[0].lower(), reverse=reverse)


### Popup
def add_student_popup():
    ## Opens a Pop up screen to add a new student ID.
    ## source: https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel
    popup = Toplevel(root)
    popup.title("Add Student")
    popup.geometry("300x150")

    Label(popup, text="Student ID:").pack(pady=(15, 2))
    entry = Entry(popup, width=30)
    entry.pack()

    def save():
        if add_student(entry.get().strip()):
            messagebox.showinfo("Success", f"Student '{entry.get().strip()}' added.")
            popup.destroy()

    Button(popup, text="Save", width=15, command=save).pack(pady=10)


def delete_student_popup():
    ## Opens a Pop up window to remove a student ID, requiring confirmation
    popup = Toplevel(root)
    popup.title("Delete Student")
    popup.geometry("300x150")

    Label(popup, text="Student ID:").pack(pady=(15, 2))
    entry = Entry(popup, width=30)
    entry.pack()

    def delete():
        sid = entry.get().strip()
        if not check_student_id(sid):
            return
        confirm = messagebox.askyesno("Confirm", f"Delete student '{sid}'?")
        if confirm:                       # if input yes delete
            if delete_student(sid):
                messagebox.showinfo("Deleted", f"Student '{sid}' removed.")
                popup.destroy()

    Button(popup, text="Delete", width=15, command=delete).pack(pady=10)


def add_grade_popupss():
####### Open pop up screen for update or add new grade
    popup = Toplevel(root)
    popup.title("Add / Update Grade")
    popup.geometry("300x230")

    Label(popup, text="Student ID:").pack(pady=(15, 2))
    sid = Entry(popup, width=30)
    sid.pack()

    Label(popup, text="Subject:").pack(pady=(8, 2))
    sub = Entry(popup, width=30)
    sub.pack()

    Label(popup, text="Grade (0-100):").pack(pady=(8, 2))
    grd = Entry(popup, width=30)
    grd.pack()

    def save():
        if add_grade(sid.get().strip(), sub.get().strip(), grd.get().strip()):
            messagebox.showinfo("Success", "Grade saved.")
            popup.destroy()

    Button(popup, text="Save", width=15, command=save).pack(pady=10)


def attendance_popup():
## this page for set attendace %
    popupss = Toplevel(root)
    popupss.title("Set Attendance")
    popupss.geometry("300x180")

    Label(popupss, text="Student ID:").pack(pady=(15, 2))
    sid = Entry(popupss, width=30)
    sid.pack()

    Label(popupss, text="Attendance % (0-100):").pack(pady=(8, 2))
    att = Entry(popupss, width=30)
    att.pack()

    def save():
        if set_attendance(sid.get().strip(), att.get().strip()):
            messagebox.showinfo("Success", "Attendance updated.")
            popupss.destroy()

    Button(popupss, text="Save", width=15, command=save).pack(pady=10)


def show_students_popupss():

    ## source: https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
    ## Displays a sortable and searchable table containing all student data.
    ## source: https://stackoverflow.com/questions/22432814/ttk-treeview-with-scrollbar
    popupssz = Toplevel(root)
    popupssz.title("All Students")
    popupssz.geometry("620x420")

    # Top frame Search + sorting areas 
    frame_top = Frame(popupssz)
    frame_top.pack(fill=X, padx=10, pady=8)    # fill=X -- cover all horizontal lines
    Label(frame_top, text="Search:").pack(side=LEFT)
    search_entry = Entry(frame_top, width=25)
    search_entry.pack(side=LEFT, padx=5)

    sort_var = StringVar(value="id")
    Label(frame_top, text="Sort by:").pack(side=LEFT, padx=(10, 2))
    sort_menu = ttk.Combobox(frame_top, textvariable=sort_var,values=["id", "average", "attendance"],width=12, state="readonly")
    sort_menu.pack(side=LEFT)
## https://www.pythontutorial.net/tkinter/tkinter-booleanvar/#:~:text=In%20Tkinter%2C%20the%20BooleanVar%20class,as%20a%20RadioButton%20or%20CheckButton%20.
    # BooleanVar -- Holds the True/False status of the checkbox.
    boolesnvarr = BooleanVar(value=False)
    Checkbutton(frame_top, text="Descending", variable=boolesnvarr).pack(side=LEFT, padx=5)

    # Define table columns and set their sizes.
    colums = ("Student ID", "Avg Grade", "Letter", "Attendance %", "Subjects")
    ## https://pythonassets.com/posts/treeview-in-tk-tkinter/
    tree = ttk.Treeview(popupssz, columns=colums, show="headings", height=15)
    for col in colums:
        tree.heading(col, text=col)             # Collumn name
        tree.column(col, width=110, anchor=CENTER)
    tree.column("Student ID", width=130)
    tree.column("Subjects",   width=140)

    # Connect the scrollbar to the table -- vertical scrolling is synchronized with yscroll.
    scrollbar = ttk.Scrollbar(popupssz, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=5)
    scrollbar.pack(side=LEFT, fill=Y, pady=5)

    def refresh_table():
        #Clears and re-populates the table based on current filters and sorting.
        for row in tree.get_children():         # Remove all lines
            tree.delete(row)

        search_filtring_inputs = search_entry.get().strip()
        if search_filtring_inputs:
            data  = search_students(search_filtring_inputs)
            items = sort_students(by=sort_var.get(), reverse=boolesnvarr.get())
            items = [(sid, d) for sid, d in items if sid in data]  # Search filter
        else:
            items = sort_students(by=sort_var.get(), reverse=boolesnvarr.get())

        for sid, sdata in items:
            avg         = calculate_average(sid)
            letter      = get_letter_grade(avg)
            att         = sdata.get("attendance", 0)
            grades_dict = sdata.get("grades", {})
            subjects    = ", ".join(grades_dict.keys()) if grades_dict else "—"
            # tree.insert("", END, ...) -- adds a new row to the end of the table
            tree.insert("", END, values=(sid, f"{avg:.1f}", letter, f"{att:.1f}%", subjects))

    refresh_table()    # When screen open table insert refreshed

    btn_frame = Frame(popupssz)
    btn_frame.pack(pady=5)
    Button(btn_frame, text="Refresh", command=refresh_table).pack(side=LEFT, padx=5)
    Button(btn_frame, text="Close",   command=popupssz.destroy).pack(side=LEFT, padx=5)

    # automatic renewal
    search_entry.bind("<KeyRelease>", lambda e: refresh_table())          # Every key press
    sort_menu.bind("<<ComboboxSelected>>", lambda e: refresh_table())     # sorting changes
    boolesnvarr.trace_add("write", lambda *args: refresh_table())           # checkbox changess


# mathlolib chart areas
######## source: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html

#https://stackoverflow.com/questions/66736758/python-3-9-difference-list-sortreverse-true-and-list-reverse
###### source: https://matplotlib.org/stable/gallery/text_labels_and_annotations/text_demo.html

def show_student_graph():
    items = sort_students(by="average", reverse=True)   # High to low sorting
    if not items:
        messagebox.showerror("Error", "No student data to display.")
        return

    names  = [sid for sid, _ in items]
    avgs   = [calculate_average(sid) for sid in names]
  
    plt.figure(figsize=(max(6, len(names)), 5))
    bars = plt.bar(names, avgs)
    plt.title("Student Grade Averages")
    plt.xlabel("Student ID")
    plt.ylabel("Average Grade")
    plt.ylim(0, 105)
    plt.xticks(rotation=30, ha="right")
    for bar, avg in zip(bars, avgs):
        ##https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
        plt.text(bar.get_x() + bar.get_width() / 2,bar.get_height() + 1,f"{avg:.1f}",ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    plt.show()

def show_subject_graph():
    ## Generates a chart showing the average grade across the school for each subject.
    data = load_datajsonss()
    subject_totals = {}   # Total grade for each course
    subject_counts = {}   # total student for each course

    for sid in data:
        for sub, grade in data[sid].get("grades", {}).items():
            subject_totals[sub] = subject_totals.get(sub, 0) + grade
            subject_counts[sub] = subject_counts.get(sub, 0) + 1

    if not subject_totals:
        messagebox.showerror("Error", "No subject data to display.")
        return

    subjects  = list(subject_totals.keys())
    averages  = [subject_totals[s] / subject_counts[s] for s in subjects]

    plt.figure(figsize=(max(6, len(subjects)), 5))
    bars = plt.bar(subjects, averages, color="steelblue")
    plt.title("Average Grade by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Grade")
    plt.ylim(0, 105)
    plt.xticks(rotation=30, ha="right")
    for bar, avg in zip(bars, averages):
        plt.text(bar.get_x() + bar.get_width() / 2,bar.get_height() + 1,f"{avg:.1f}",ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    plt.show()

def show_school_avg():
### Shows school avarage
    avg    = school_average()
    letter = get_letter_grade(avg)
    messagebox.showinfo("School Average", f"Overall School Average: {avg:.2f} ({letter})")

##### Main Screeeen
### Main Label
Label(root, text="Student Progress Tracker",).pack(pady=(20, 5))
Label(root, text="Students",).pack(pady=(0, 5))
Button(root, text="Add Student",       width=22, command=add_student_popup).pack(pady=4)
Button(root, text="Delete Student",    width=22, command=delete_student_popup).pack(pady=4)
Button(root, text="Show All Students", width=22, command=show_students_popupss).pack(pady=4)
Label(root, text="Grades & Attendance").pack(pady=(0, 5))
Button(root, text="Add / Update Grade", width=22, command=add_grade_popupss).pack(pady=4)
Button(root, text="Set Attendance",     width=22, command=attendance_popup).pack(pady=4)
Button(root, text="School Average",     width=22, command=show_school_avg).pack(pady=4)
Label(root, text="Reports & Charts",).pack(pady=(20, 5))
Button(root, text="Student Grade Chart",   width=25, command=show_student_graph).pack(pady=4)
Button(root, text="Subject Average Chart", width=25, command=show_subject_graph).pack(pady=4)

# ## source: https://docs.python.org/3/library/tkinter.html#tkinter.Misc.mainloop
root.mainloop()