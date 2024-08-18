import os
import sys
import warnings
import numpy as np
import pandas as pd

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Student import Student
from Class import Class

# hide openpxyl spreadsheet warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simmons Student Class Hub")
        layout = QGridLayout()
        self.setLayout(layout)
        self.setContentsMargins(30, 30, 30, 30)

        self.studentName = "Lee"

        # for c in range(len(studentClasses)):
        #     layout.addWidget(QLabel(str(studentClasses[c])), c, 0, Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(studentClasses, 0, 0)

    def findStudent(self, name):
        pass
    #     for stud in s:
    #         if stud.name == name:
    #             return stud.classes
        
def getStudentNameFromDF():
    students = {}
    # for spreadsheets in folder
    for f in os.listdir('./spreadsheets'):
        # file name becomes student name
        name = f.split(".")[0]
        # get cd to find filepath
        cd = os.getcwd()
        students[name] = pd.read_excel(cd+"/spreadsheets/"+f, skiprows=2)
    return students

def convertDOW(dow):
    dayToNum = {"M": 0, "T": 1, "W": 2, "Th": 3, "F": 4}
    numDOW = []
    for day in dow:
        numDOW.append(dayToNum[day])
    return numDOW

def convertTimeToDatetime(cTime):
    # split time from AM/PM
    timeSplit = cTime.split()
    pm = 0
    if timeSplit[1] == "PM":
        if "12" not in timeSplit[0]:
            # convert to miltary time if not 12pm
            pm = 12
    # split hours and mintues
    timeSplitAgain = timeSplit[0].split(":")
    hours = int(timeSplitAgain[0]) + pm
    minutes = int(timeSplitAgain[1])
    cTime = pd.to_datetime(f"{hours}:{minutes}:00", format="%H:%M:%S")
    return cTime

def createClass(row):
    name = row["Course Listing"].split("-")[0]
    fullName = row["Course Listing"].split("-")[1]
    prof = row["Instructor"]
    # turn days of week into list
    timeData = row["Meeting Patterns"]
    if type(timeData) != float:
        dow = convertDOW(timeData.split(" |")[0].split("/"))
        tStart = convertTimeToDatetime(timeData.split("|")[1].split("-")[0])
        tEnd = convertTimeToDatetime(timeData.split("|")[1].split("-")[1])
    else:
        dow = None
        tStart = None
        tEnd = None
    dStart = row["Start Date"]
    dEnd = row["End Date"]
    loc = row["Delivery Mode"]
    return Class(name, fullName, prof, dow, tStart, tEnd, dStart, dEnd, loc)

def searchAppendClasses(row, classes, stud):
    name = row["Course Listing"].split("-")[0]
    hasClass = False
    for c in classes:
        if hasClass == False and name == c.getName():
            # append student/class to each other
            c.appendStudent(stud)
            stud.appendClass(c)
            hasClass = True
    if hasClass == False:
        # create new class if not already present
        newClass = createClass(row)
        classes.append(newClass)
        newClass.appendStudent(stud)
        stud.appendClass(newClass)
    return classes

def createStudent(name):
    stud = Student(name)
    return stud

def main():
    studentNameDF = getStudentNameFromDF()
    students = []
    classes = []
    for name, df in studentNameDF.items():
        stud = createStudent(name)
        for index, row in df.iterrows():
            # see if class was already created
            classes = searchAppendClasses(row, classes, stud)
        students.append(stud)
        stud.getOrderedClasses()
    currentDate = pd.Timestamp(2024, 9, 4)
    currentTime = pd.to_datetime("13:00:00", format="%H:%M:%S")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



    # for c in classes:
    #     if c.dow is not None and c.dStart <= currentDate <= c.dEnd and currentDate.dayofweek in c.dow:
    #         if c.tStart is not None and c.tStart <= currentTime <= c.tEnd:
    #             print(c.name)
    #             print(*c.students)
    
main()


# pull name from file
# view students upcoming classes for day
# select student to view their classes for day and what you share with them
# gui lmao
