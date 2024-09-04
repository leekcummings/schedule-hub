from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self, studName):
        super().__init__()

        self.setWindowTitle("Simmons Student Class Hub")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(30)

        self.studentName = studName

        # Datetime info
        # self.label1 = QLabel(str(pd.Timestamp(2024, 9, 4).date()))
        # self.layout.addWidget(self.label1, 0, 0, Qt.AlignmentFlag.AlignCenter)
        # self.label2 = QLabel(str(pd.to_datetime("13:00:00", format="%H:%M:%S").time()))
        # self.layout.addWidget(self.label2, 1, 0, Qt.AlignmentFlag.AlignCenter)

    def getCoursePositionString(self, course, time):
        if course.tStart <= time <= course.tEnd:
            label = "Current Course:"
        elif course.tStart > time: 
            label = "Upcoming Course:"
        else:
            label = "Previous Course:"
        return label

    def addStudentsToClasses(self, course):
        hBox = QHBoxLayout()
        self.courseLayout.addLayout(hBox)

        for stud in course.students:
            if stud.name != self.studentName:
                hBox.addWidget(QLabel(str(stud)))
            else:
                hBox.addWidget(QLabel(str("Me!")))

    def createCourseWidget(self, course, time):
        label = self.getCoursePositionString(course, time)
        self.courseLayout.addWidget(QLabel(label))
        self.courseLayout.addWidget(QLabel(str(course.name)))
        self.addStudentsToClasses(course)

    def addCoursesLayout(self, date, time):
        self.courseLayout = QVBoxLayout()
        self.layout.addLayout(self.courseLayout, 0, 0)
        # only display today's courses
        for course in self.dowCourses[date.dayofweek]:
            if course.dStart <= date.date() <= course.dEnd:
                self.createCourseWidget(course, time)
                              
    def addFriendsLayout(self, date, time, students):
        # seperated layout for friend information
        self.friendsTab = QVBoxLayout()
        self.layout.addLayout(self.friendsTab, 0, 3)

    def updateStudent(self, s):
        self.student = s
        self.courses = s.courses
        self.dowCourses = s.dowCourses

    def findStudent(self, name, s):
        for stud in s:
            if str(stud.name) == name:
                self.updateStudent(stud)
