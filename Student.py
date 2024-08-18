from Course import Course

class Student:
    def __init__(self, name) -> None:
        self.__name = name
        self.__courses = []
        self.__currentCourse = None
        self.coursesByDOW()


    def coursesByDOW(self):
        self.__dowCourses = {}
        for dow in range(0, 5):
            self.__dowCourses[dow] = []
        for cName in self.__courses:
            cObject = cName.getCourseObject()
            dowList = cObject.getDOW()
            if dowList is not None:
                for dow in dowList:
                    self.__dowCourses[dow].append(cObject)
        for dow, courses in self.__dowCourses.items():
            courses.sort(key = lambda x: x.getTStart())

    def getName(self):
        return self.__name

    def getCourses(self):
        return self.__courses
    
    def appendCourse(self, c):
        self.__courses.append(c)
        self.coursesByDOW()

    def __str__(self) -> str:
        return self.__name