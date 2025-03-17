#Importing necessary modules
from tkinter import*
import xml.dom.minidom
from datetime import*
import math

#XML
file = xml.dom.minidom.parse('data.xml')
group = file.documentElement

#Creating The Window
window = Tk()
window.title("To Do List")
window.configure(bg = "#dfeaee")
window.geometry("950x450")

#Creating Widget
maintitle = Label(window, text = "TO DO LIST", font = "Arial 18 bold", background = "#dfeaee", anchor = "w", justify = "left")
todaylist = Label(window, text = "Today's List", font = "Tahoma 15 bold", foreground = "#b25998", background = "#dfeaee")
addtasktitle = Label(window, text = "Add Task", font = "Tahoma 15 bold", foreground = "#b25998", width = 30, background = "#dfeaee", anchor = "w", justify = "left")
addtask = Label(window, text = "Task", font = "Tahoma 12", width = 30, background = "#dfeaee", anchor = "w", justify = "left")
taskin = Entry(window, width = 50)
addbutton = Button(window, text = "ADD", font = "Tahoma 10 bold", width = 15, background = "#ddcfdd")
listtitle = Label(window, text = "List of Task", font = "Tahoma 15 bold", foreground = "#b25998", width = 30, background = "#dfeaee", anchor = "w", justify = "left")
delbutton = Button(window, text = "DELETE", font = "Tahoma 10 bold", width = 15, background = "#ddcfdd")
donebutton = Button(window, text = "DONE", font = "Tahoma 10 bold", width = 15, background = "#ddcfdd")
tasklist = Listbox(window, width = 70, height = 15, font = "Tahoma 10", background = "#dfeaee", border = 0)
progress = Label(window, width = 70, height = 1, background = "white", relief = "solid", borderwidth = 1)
progressbar = Label(window, background = "#529742", relief = "solid", borderwidth = 1)
progresstiitle = Label(window, background = "#dfeaee", font = "Tahoma 10")

#Count Progress
def countprogress():
    todaydate = date.today()
    todaydate = date.strftime(todaydate, "%d")
    task = group.getElementsByTagName('date')
    
    total = 0
    for t in task:
        taskdate = t.getAttribute('id')
        if taskdate == todaydate:
            total = total + 1
    
    count = 0
    for t in task:
        taskdate = t.getAttribute('id')
        status = t.getElementsByTagName('status')[0].childNodes[0].data
        if taskdate == todaydate and status == '\u2714' :
            count = count + 1

    percentage = 0
    if count != 0 and total != 0:
        widthbar = math.ceil(count / total * 70)
        percentage = math.ceil(count / total * 100)
        progressbar.configure(width = widthbar)
    
    if percentage >= 0 and percentage <= 30:
        progressbar.configure(bg = "#FF3333")
    elif percentage >= 31 and percentage <= 50:
        progressbar.configure(bg = "#FFCC00")
    elif percentage >= 51 and percentage <= 70:
        progressbar.configure(bg = "#FFFF00")
    elif percentage >= 71 and percentage <= 89:
        progressbar.configure(bg = "#99FFCC")
    elif percentage >= 90 and percentage <= 100:
        progressbar.configure(bg = "#00CC00")
    progresstiitle.configure(text = "Task " + str(count) + " / " + str(total) + " (" + str(percentage) + "%)")

#Display Today's Task
def todaytask():
    tasklist.delete(0, END)
    todaydate = date.today()
    todaydate = date.strftime(todaydate, "%d")
    task = group.getElementsByTagName('date')
    for t in task:
        taskdate = t.getAttribute('id')
        if int(taskdate) == int(todaydate):
            taskstatus = t.getElementsByTagName('status')[0].childNodes[0].data
            tasktitle = t.getElementsByTagName('task')[0].childNodes[0].data
            tasklist.insert(1, taskstatus + "     " + tasktitle)

#Add Task to the List
def addlist():
    taskname = taskin.get()
    todaydate = date.today()
    todaydate = date.strftime(todaydate, "%d")

    task = group.getElementsByTagName('task')
    taskcount = 1
    for count in task:
        if count.hasAttribute('id'):
            taskcount = count.getAttribute('id')
            taskcount = int(taskcount) + 1
    
    newtask = file.createElement('date')
    newtask.setAttribute('id', str(todaydate))

    nametask = file.createElement('task')
    nametask.setAttribute('id', str(taskcount))
    nametask.appendChild(file.createTextNode(taskname))

    status = file.createElement('status')
    status.appendChild(file.createTextNode('\u25a2'))

    newtask.appendChild(nametask)
    newtask.appendChild(status)

    group.appendChild(newtask)
    with open('data.xml', 'w', encoding='utf-8') as f:
        file.writexml(f)
    
    todaytask()
    countprogress()

#Delete Task from the List
def dellist():
    select = tasklist.get(tasklist.curselection())
    task = str(select.split(" ", 1)[1])
    task = task.lstrip()
    todaydate = date.today()
    todaydate = date.strftime(todaydate, "%d")
    tasks = group.getElementsByTagName('date')
    
    for id, t in enumerate(tasks):
        checkdate = t.getAttribute('id')
        checktask = t.getElementsByTagName('task')[0].childNodes[0].data
        if todaydate == checkdate and task == checktask:
            remove = group.getElementsByTagName('date')[id]
            remove.parentNode.removeChild(remove)
    
    with open('data.xml', 'w', encoding='utf-8') as f:
        file.writexml(f)
    
    todaytask()
    countprogress()

#Function to set Done on a Task
def done():
    select = tasklist.get(tasklist.curselection())
    task = str(select.split(" ", 1)[1])
    task = task.lstrip()
    todaydate = date.today()
    todaydate = date.strftime(todaydate, "%d")
    tasks = group.getElementsByTagName('date')
    
    for id, t in enumerate(tasks):
        checkdate = t.getAttribute('id')
        checktask = t.getElementsByTagName('task')[0].childNodes[0].data
        if todaydate == checkdate and task == checktask:
            t.getElementsByTagName('status')[0].childNodes[0].nodeValue = "\u2714"
    
    with open('data.xml', 'w', encoding='utf-8') as f:
        file.writexml(f)
    
    todaytask()
    countprogress()

#Positions
maintitle.place(x = 20, y = 10)
todaylist.place(x = 20, y = 50)
progress.place(x = 20, y = 90)
progressbar.place(x = 20, y = 90)
progresstiitle.place(x = 20, y = 115)
donebutton.place(x = 20, y = 135)
tasklist.place(x = 20, y = 175)
addtasktitle.place(x = 550, y = 50)
addtask.place(x = 550, y = 90)
taskin.place(x = 550, y = 115)
addbutton.place(x = 550, y = 145)
delbutton.place(x = 200, y = 135)

#Getting Rid of Old Task
todaydate = date.today()
todaydate = date.strftime(todaydate, "%d")
tasks = group.getElementsByTagName('date')
for id, t in enumerate(tasks):
    taskdate = t.getAttribute('id')
    if todaydate == taskdate:
        #Functions to run when the program starts
        todaytask()
        countprogress()
    else:
        remove = tasks[id]
        remove.parentNode.removeChild(remove)
with open('data.xml', 'w', encoding='utf-8') as f:
    file.writexml(f)        

#Button Functions
addbutton.configure(command = addlist)
delbutton.configure(command = dellist)
donebutton.configure(command = done)

#Keeping the window open
window.resizable(0,0)
window.mainloop()