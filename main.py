import sys
import json
import warnings
import numpy as np
import pandas as pd
 
from PyQt6.QtWidgets import QApplication

import launch
import readExcel

from Student import Student
from Course import Course
from MainWindow import MainWindow

# hide openpxyl spreadsheet warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
 
def createStudent(name):
    stud = Student(name)
    return stud

def main():
    launch.intialLaunch()
    students = []
    courses = []

    studentNameDF = launch.getStudentNameFromDF()
    selectedName = launch.selectSelfName(studentNameDF)
        
    for name, df in studentNameDF.items():
        stud = createStudent(name)
        for index, row in df.iterrows():
            courses = readExcel.searchAppendCourses(row, courses, stud)
        students.append(stud)
        stud.coursesByDOW() # probably change so it only runs on user, not all students

    # TEMP DATETIME
    # currentDate = pd.Timestamp("today") # don't add .date(), it breaks later code
    currentDate = pd.Timestamp("today")
    currentTime = pd.to_datetime("today", format="%H:%M:%S").time()

    # create PyQt6 application
    app = QApplication(sys.argv)
    window = MainWindow(selectedName)
    window.show()

    # add widgets to window
    window.findStudent(window.studentName, students)
    window.addCoursesLayout(currentDate, currentTime)
    window.addFriendsLayout(currentDate, currentTime, students)

    sys.exit(app.exec())
    
main()

# work on json settings
# create Job(Event)