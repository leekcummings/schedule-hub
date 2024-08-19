from Student import Student
from Course import Course

import os
import sys
import warnings
import numpy as np
import pandas as pd

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# hide openpxyl spreadsheet warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simmons Student Class Hub")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(30, 30, 30, 30)

        self.studentName = "Lee"

        # Datetime info
        # self.label1 = QLabel(str(pd.Timestamp(2024, 9, 4).date()))
        # self.layout.addWidget(self.label1, 0, 0, Qt.AlignmentFlag.AlignCenter)
        # self.label2 = QLabel(str(pd.to_datetime("13:00:00", format="%H:%M:%S").time()))
        # self.layout.addWidget(self.label2, 1, 0, Qt.AlignmentFlag.AlignCenter)

    def addCoursesLayout(self, date, time):
        counter = 0
        for course in self.dowCourses[date.dayofweek]:
            if course.dStart <= date.date() <= course.dEnd:
                if course.tStart <= time <= course.tEnd:
                    currentCourse = QLabel("Current Course")
                    currentCourse.setContentsMargins(30, 60, 30, 60)
                    self.layout.addWidget(currentCourse, counter+2, 0, 
                        Qt.AlignmentFlag.AlignCenter)
                    self.layout.addWidget(QLabel(str(course)), counter+2, 1, 
                        Qt.AlignmentFlag.AlignCenter)
                    counter += 1
                    vBox = QHBoxLayout()
                    self.layout.addLayout(vBox, counter+2, 0, 1, 2)
                    for stud in course.students:
                        vBox.addWidget(QLabel(str(stud)))
                        counter += 1
                elif course.tStart > time:
                    self.layout.addWidget(QLabel("Upcoming Course"), counter+2, 0, 
                    Qt.AlignmentFlag.AlignCenter)
                    self.layout.addWidget(QLabel(str(course)), counter+2, 1, 
                        Qt.AlignmentFlag.AlignCenter)
                    counter += 1
                else:
                    self.layout.addWidget(QLabel("Previous Course"), counter+2, 0, 
                    Qt.AlignmentFlag.AlignCenter)
                    self.layout.addWidget(QLabel(str(course)), counter+2, 1, 
                        Qt.AlignmentFlag.AlignCenter)
                    counter += 1
          
    def addFriendsLayout(self, date, time, students):
        counter = 2
        for stud in students:
            if stud.name != self.studentName:
                for course in self.dowCourses[date.dayofweek]:
                    if (course.dStart <= date.date() <= course.dEnd) and (course.tStart <= time <= course.tEnd):
                        self.layout.addWidget(QLabel(str(stud)), counter, 3, Qt.AlignmentFlag.AlignCenter)
                        self.layout.addWidget(QLabel(str(course)), counter, 4, Qt.AlignmentFlag.AlignCenter)
                        counter += 1

    def updateStudent(self, s):
        self.student = s
        self.courses = s.courses
        self.dowCourses = s.dowCourses

    def findStudent(self, name, s):
        for stud in s:
            if str(stud.name) == name:
                self.updateStudent(stud)
        
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
    # dayToNum based on pandas .dayofweek()
    # convert each DOW abbreviation to num
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

    cTime = pd.to_datetime(f"{hours}:{minutes}:00", format="%H:%M:%S").time()
    return cTime

def createCourse(row):
    # retrieve information from .xlsx columns 
    name = row["Course Listing"].split("-")[0]
    fullName = row["Course Listing"].split("-")[1]
    prof = row["Instructor"]

    # turn days of week into list
    timeData = row["Meeting Patterns"]
    # if timeData not a float from .xlsx, it's NoneType
    if type(timeData) != float:
        dow = convertDOW(timeData.split(" |")[0].split("/"))
        tStart = convertTimeToDatetime(timeData.split("|")[1].split("-")[0])
        tEnd = convertTimeToDatetime(timeData.split("|")[1].split("-")[1])
    else:
        dow = None
        tStart = None
        tEnd = None

    dStart = row["Start Date"].date()
    dEnd = row["End Date"].date()
    loc = row["Delivery Mode"]
    return Course(name, fullName, prof, dow, tStart, tEnd, dStart, dEnd, loc)

def searchAppendCourses(row, courses, stud):
    # get class name from row
    name = row["Course Listing"].split("-")[0]
    hasCourse = False
    for c in courses:
        if hasCourse == False and name == c.name:
            # append student/class to each other
            c.students.append(stud)
            stud.courses.append(c)
            hasCourse = True
    if hasCourse == False:
        # create new class if not already present
        newCourse = createCourse(row)
        
        # more appending to each other
        courses.append(newCourse)
        newCourse.students.append(stud)
        stud.courses.append(newCourse)
    return courses

def createStudent(name):
    stud = Student(name)
    return stud

def main():
    students = []
    courses = []

    studentNameDF = getStudentNameFromDF()

    for name, df in studentNameDF.items():
        stud = createStudent(name)
        for index, row in df.iterrows():
            courses = searchAppendCourses(row, courses, stud)
        students.append(stud)
        stud.coursesByDOW() # probably change so it only runs on user, not all students

    # TEMP DATETIME
    currentDate = pd.Timestamp(2024, 9, 4) # don't add .date(), it breaks later code
    currentTime = pd.to_datetime("13:00:00", format="%H:%M:%S").time()

    # create PyQt6 application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # add widgets to window
    window.findStudent(window.studentName, students)
    window.addCoursesLayout(currentDate, currentTime)
    window.addFriendsLayout(currentDate, currentTime, students)

    sys.exit(app.exec())
    
main()