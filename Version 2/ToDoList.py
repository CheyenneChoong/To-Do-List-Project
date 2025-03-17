# Import built-in module for the window interface.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import math

try: # Creates the text file for storage if not created.
    file = open('tasks.txt', 'a')
    file.close()
except: # Error message for if any issues.
    print('Error in file.')

# Base for the window.
window = tk.Tk()
window.withdraw()
window.title('To Do List')
window.geometry('900x450')
window.configure(background = 'white')

# Navigation widgets.
navigationBackground = tk.Frame(window, width = 220, height = 450, background = '#F2CFEE')
navigationBackground.place(x = 0, y = 0)
addTaskPageButton = tk.Button(window, text = 'ADD TASK', font = 'Tahoma 10 bold', width = 20, height = 1, background = '#CCECFF')
addTaskPageButton.place(x = 20, y = 30)
todayListButton = tk.Button(window, text = 'TODAY\'S TASK', font = 'Tahoma 10 bold', width = 20, height = 1, background = '#CCECFF')
todayListButton.place(x = 20, y = 70)
allTaskButton = tk.Button(window, text = 'ALL TASK', font = 'Tahoma 10 bold', width = 20, height = 1, background = '#CCECFF')
allTaskButton.place(x = 20, y = 110)

# Main frame for content area.
mainFrame = tk.Frame(window, background = 'white', width = 680, height = 450)
mainFrame.place(x = 220, y = 0)

# Add Task Page Widgets.
addTaskPageTitle = tk.Label(mainFrame, text = 'ADD TASK', font = 'Tahoma 12 bold', background = 'white')
dateInputLabel = tk.Label(mainFrame, text = 'DATE', font = 'Arial 10', background = 'white')
dateInput = tk.Entry(mainFrame, relief = 'solid')
taskInputLabel = tk.Label(mainFrame, text = 'TASK', font = 'Arial 10', background = 'white')
taskInput = tk.Entry(mainFrame, width = 20, relief = 'solid')
addTaskAddButton = tk.Button(mainFrame, text = 'ADD', font = 'Tahoma 10 bold', background = '#D9F2D0')
addTaskUpdateButton = tk.Button(mainFrame, text = 'UPDATE', font = 'Tahoma 10 bold', background = '#FFFFCC')
addTaskDeleteButton = tk.Button(mainFrame, text = 'DELETE', font = 'Tahoma 10 bold', background = '#FBE3D6')
addTaskList = ttk.Treeview(mainFrame, columns = ('date', 'task'), show = 'headings')
addTaskList.heading('task', text = 'Task')
addTaskList.heading('date', text = 'Date')
addTaskList.column('task', width = 560)
addTaskList.column('date', width = 100)

# All Task Page Widgets.
allTaskPageTitle = tk.Label(mainFrame, text = 'ALL TASKS', font = 'Tahoma 12 bold', background = 'white')
removeTaskButton = tk.Button(mainFrame, text = 'REMOVE OLD TASK', font = 'Arial 10 bold', background = '#FBE3D6')
allTaskFilterLabel = tk.Label(mainFrame, text = 'DATE', font = 'Arial 10', background = 'white')
allTaskFilterInput = tk.Entry(mainFrame, relief = 'solid')
allTaskFilterButton = tk.Button(mainFrame, text = 'FILTER',font = 'Tahoma 10 bold', background = '#CAEEFB')
allTaskList = ttk.Treeview(mainFrame, columns = ('task', 'date'), show = 'headings')
allTaskList.heading('task', text = 'Task')
allTaskList.heading('date', text = 'Date')
allTaskList.column('task', width = 560)
allTaskList.column('date', width = 100)

# Today's Task Page Widgets.
todayTaskPageTitle = tk.Label(mainFrame, text = 'TODAY\'S TASK', font = 'Tahoma 12 bold', background = 'white')
progressBarBase = tk.Label(mainFrame, width = 90, background = 'white', relief = 'solid')
progressBar = tk.Label(mainFrame, width = 90, relief = 'solid', background = '#FF3333')
progressLabel = tk.Label(mainFrame, text = 'Progress : ', font = 'Arial 10', background = 'white')
todayTaskList = ttk.Treeview(mainFrame, columns = ('task'), show = 'headings')
todayTaskList.heading('task', text = 'Task')

def readFile(): # Function to read all the tasks in the text file.
    taskList = [] # List to store all the tasks.
    with open('tasks.txt', 'r') as taskFile:
        for line in taskFile: # Reads every single line of the task.
            line = line.strip('\n').split('; ')
            task = {'taskID' : line[0], 'taskName' : line[1], 'taskDate' : line[2], 'taskStatus' : line[3]}
            taskList.append(task)
    return taskList # Return the task list.

def singleTask(taskID): # Function to retrieve a single line of information.
    taskList = readFile() # Reads all the task.
    for task in taskList: # Finds and return the task searched for.
        if task['taskID'] == taskID:
            return task

def addTask(): # Function to add a new task.
    # Gather the inputs.
    taskDate = dateInput.get()
    taskName = taskInput.get()
    # Validates the date.
    try:
        time.strptime(taskDate, '%d-%m-%Y')
    except:
        messagebox.showerror('Error', 'Invalid Date.')
        return
    # Ensures the input for the task name is not empty.
    if not taskName:
        messagebox.showerror('Error', 'Please enter a task.')
        return

    taskList = readFile() # Reads all the task in the storage.
    count = 1 # The task count.
    for task in taskList:
        if task['taskDate'] == taskDate:
            count += 1
    taskID = taskDate.replace('-', '') + str(count) # Create unique ID.
    newTask = f'{taskID}; {taskName}; {taskDate}; pending\n' # Format of storage.
    with open('tasks.txt', 'a') as taskFile: # Storing of data.
        taskFile.write(newTask)
    addTaskPage() # Refresh the page.

def updateTask(): # Function to update an existing task.
    # Gather the inputs.
    taskID = ''.join(addTaskList.selection())
    taskDate = dateInput.get()
    taskName = taskInput.get()

    # Validates the date.
    try:
        time.strptime(taskDate, '%d-%m-%Y')
    except:
        messagebox.showerror('Error', 'Invalid Date.')
        return
    # Ensures the input for the task name is not empty.
    if not taskName:
        messagebox.showerror('Error', 'Please enter a task.')
        return

    oldData = singleTask(taskID)
    taskList = readFile() # Reads all the task in the storage.

    if oldData['taskDate'] == taskDate: # Checks if there is a need to change ID.
        newTaskID = taskID
    else:
        count = 1 # The task count.
        for task in taskList:
            if task['taskDate'] == taskDate:
                count += 1
        newTaskID = taskDate.replace('-', '') + str(count)
    
    with open('tasks.txt', 'a') as taskFile: # Writes the update into the file.
        taskFile.truncate(0)
        for task in taskList:
            if task['taskID'] == taskID:
                task = f'{newTaskID}; {taskName}; {taskDate}; {task['taskStatus']}\n'
                taskFile.write(task)
            else:
                taskFile.write('; '.join(task.values()) + '\n')
    addTaskPage() # Refresh the page.

def removeTask(): # Function to remove an existing task.
    taskID = ''.join(addTaskList.selection()) # Retrieves the ID of the task to delete.
    response = messagebox.askquestion('Delete', 'Do you want to delete this task?') # Confirm.
    if response == 'no': 
        return
    taskList = readFile() # Read all the task
    with open('tasks.txt', 'a') as taskFile: # Save the new changes.
        taskFile.truncate(0)
        for task in taskList:
            if task['taskID'] != taskID:
                task = '; '.join(task.values()) + '\n'
                taskFile.write(task)
    addTaskPage() # Refresh the page.

def removeOldTask(): # Function to remove old task.
    taskList = readFile() # Reads all the task. 
    todayDate = time.localtime() # Retrieve information about today's task.
    todayDate = time.strftime('%d-%m-%Y', todayDate) 
    with open('tasks.txt', 'a') as taskFile:
        taskFile.truncate(0) # Clears the file.
        for task in taskList:
            taskDate = task['taskDate'] # Find the task that is on a day that passed.
            check = int(todayDate.replace('-', '')) - int(taskDate.replace('-', ''))
            if check <= 0:
                task = '; '.join(task.values()) + '\n'
                taskFile.write(task)
    allTaskPage() # Refresh the page.

def filterTask(): # Function to filter the tasks.
    taskDate = allTaskFilterInput.get()
    for task in allTaskList.get_children():
        allTaskList.delete(task)
    
    taskList = readFile()

    # Validates the date.
    try:
        time.strptime(taskDate, '%d-%m-%Y')
    except:
        for task in taskList:
            if task['taskStatus'] == 'pending':
                taskName = f'\u25a2   {task['taskName']}'
            else:
                taskName = f'\u2714   {task['taskName']}'
            allTaskList.insert(parent = '', index = 'end', iid = task['taskID'], values = (taskName, task['taskDate'],))
        return

    for task in taskList:
        if task['taskDate'] == taskDate:
            if task['taskStatus'] == 'pending':
                taskName = f'\u25a2   {task['taskName']}'
            else:
                taskName = f'\u2714   {task['taskName']}'
            allTaskList.insert(parent = '', index = 'end', iid = task['taskID'], values = (taskName, task['taskDate']))

def markTask(taskID): # Function to mark a task as done or pending.
    taskList = readFile()
    with open('tasks.txt', 'a') as taskFile:
        taskFile.truncate(0)
        for task in taskList:
            if task['taskID'] == taskID:
                if task['taskStatus'] == 'pending':
                    task['taskStatus'] = 'done'
                else:
                    task['taskStatus'] = 'pending'
            taskFile.write('; '.join(task.values()) + '\n')

def addTaskPage(): # Add Task Page.
    # Remove the whatever contents already in the frame to make way for this page.
    for frame in mainFrame.winfo_children():
        frame.place_forget()
        window.update()

    # Positions of all the add task page widgets.
    addTaskPageTitle.place(x = 10, y = 10)
    dateInputLabel.place(x = 10, y = 50)
    dateInput.place(x = 10, y = 80, width = 100, height = 20)
    taskInputLabel.place(x = 130, y = 50)
    taskInput.place(x = 130, y = 80, width = 500, height = 20)
    addTaskAddButton.place(x = 10, y = 110, width = 100)
    addTaskUpdateButton.place(x = 120, y = 110, width = 100)
    addTaskDeleteButton.place(x = 230, y = 110, width = 100)
    addTaskList.place(x = 10, y = 150, width = 660, height = 280)

    # Clear the list to allow the latest updated list.
    for task in addTaskList.get_children():
        addTaskList.delete(task)

    # Display all the task.
    taskList = readFile()
    for task in taskList:
        addTaskList.insert(parent = '', index = 'end', iid = task['taskID'], values = (task['taskDate'], task['taskName'],))

# Configuring the buttons in the add task page.
addTaskAddButton.configure(command = addTask)
addTaskUpdateButton.configure(command = updateTask)
addTaskDeleteButton.configure(command = removeTask)

# Function for selecting something to update.
def onClickAddTaskPage(event):
    for selectedID in addTaskList.selection():
        selectedTask = singleTask(selectedID)
        taskInput.delete(0, tk.END)
        dateInput.delete(0, tk.END)
        taskName = selectedTask['taskName']
        taskDate = selectedTask['taskDate']
        taskInput.insert(0, taskName)
        dateInput.insert(0, taskDate)
addTaskList.bind('<<TreeviewSelect>>', onClickAddTaskPage)

def allTaskPage(): # Positions of all the all task page widgets.
    # Remove the whatever contents already in the frame to make way for this page.
    for frame in mainFrame.winfo_children(): 
        frame.place_forget()
        window.update()
    
    # Position of all the all task page widgets.
    allTaskPageTitle.place(x = 10, y = 10)
    removeTaskButton.place(x = 10, y = 50, width = 180, height = 25)
    allTaskFilterLabel.place(x = 200, y = 50)
    allTaskFilterInput.place(x = 245, y = 50, width = 100, height = 25)
    allTaskFilterButton.place(x = 355, y = 50, width = 120, height = 25)
    allTaskList.place(x = 10, y = 100, width = 660, height = 330)

    for task in allTaskList.get_children():
        allTaskList.delete(task)

    # Display all the task.
    taskList = readFile()
    for task in taskList:
        if task['taskStatus'] == 'pending':
            taskName = f'\u25a2   {task['taskName']}'
        else:
            taskName = f'\u2714   {task['taskName']}'
        allTaskList.insert(parent = '', index = 'end', iid = task['taskID'], values = (taskName, task['taskDate'],))

# Configuring the buttons in the all task page.
removeTaskButton.configure(command = removeOldTask)
allTaskFilterButton.configure(command = filterTask)

# Function for marking something when clicked.
def onClickAllTaskPage(event):
    for selectedID in allTaskList.selection():
        markTask(selectedID)
        allTaskPage()
allTaskList.bind('<<TreeviewSelect>>', onClickAllTaskPage)

def progressBarAnimation():
    todayDate = time.localtime() # Retrieve information about today's task.
    todayDate = time.strftime('%d-%m-%Y', todayDate)
    taskList = readFile()
    taskDone, totalTask = 0, 0
    for task in taskList:
        if task['taskStatus'] == 'done':
            taskDone += 1
        totalTask += 1
    widthBar, percentage = 1, 0
    if taskDone != 0 and totalTask != 0:
        widthBar = math.ceil(taskDone / totalTask * 90)
        percentage = math.ceil(taskDone / totalTask * 100)
    
    for progress in range(1, widthBar+1):
        window.update_idletasks()
        time.sleep(0.01)
        if percentage >= 0 and percentage <= 30:
            progressBar.configure(bg = "#FF3333", width = progress)
        elif percentage >= 31 and percentage <= 50:
            progressBar.configure(bg = "#FFCC00", width = progress)
        elif percentage >= 51 and percentage <= 70:
            progressBar.configure(bg = "#FFFF00", width = progress)
        elif percentage >= 71 and percentage <= 89:
            progressBar.configure(bg = "#99FFCC", width = progress)
        elif percentage >= 90 and percentage <= 100:
            progressBar.configure(bg = "#00CC00", width = progress)
    progressLabel.configure(text = "Progress : " + str(taskDone) + " / " + str(totalTask) + " (" + str(percentage) + "%)")

def todayTaskPage(): # Positions of all the today's task page widgets.
    # Remove the whatever contents already in the frame to make way for this page.
    for frame in mainFrame.winfo_children():
        if frame not in (todayTaskPageTitle, progressLabel, progressBarBase, todayTaskList):
            frame.place_forget()
            window.update()
    
    # Position of all the today's task page widgets.
    todayTaskPageTitle.place(x = 10, y = 10)
    progressBarBase.place(x = 10, y = 50)
    progressBar.place(x = 10, y = 50)
    progressLabel.place(x = 10, y = 80)
    todayTaskList.place(x = 10, y = 110, width = 660, height = 320)

    for task in todayTaskList.get_children():
        todayTaskList.delete(task)

    # Display all the task.
    taskList = readFile()
    todayDate = time.localtime()
    todayDate = time.strftime('%d-%m-%Y', todayDate)
    for task in taskList:
        if task['taskDate'] != todayDate:
            continue
        if task['taskStatus'] == 'pending':
            taskName = f'\u25a2   {task['taskName']}'
        else:
            taskName = f'\u2714   {task['taskName']}'
        todayTaskList.insert(parent = '', index = 'end', iid = task['taskID'], values = (taskName,))
    progressBarAnimation()

# Function for selecting task to mark.
def onClickTodayTaskPage(event):
    for selectedID in todayTaskList.selection():
        markTask(selectedID)
        todayTaskPage()
todayTaskList.bind('<<TreeviewSelect>>', onClickTodayTaskPage)

# Configure the navigation buttons.
addTaskPageButton.configure(command = addTaskPage)
allTaskButton.configure(command = allTaskPage)
todayListButton.configure(command = todayTaskPage)

# Initial / default page.
todayTaskPage()

# Keeps the window open for usage.
window.resizable(0, 0)
window.deiconify()
window.mainloop()