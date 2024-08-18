from Class import Class

class Student:
    def __init__(self, name) -> None:
        self.__name = name
        self.__classes = []
        self.__currentClass = None
        self.classesByDOW()


    def classesByDOW(self):
        self.__dowClasses = {}
        for dow in range(0, 5):
            self.__dowClasses[dow] = []
        for cName in self.__classes:
            cObject = cName.getClassObject()
            dowList = cObject.getDOW()
            if dowList is not None:
                for dow in dowList:
                    self.__dowClasses[dow].append(cObject)
        for dow, classes in self.__dowClasses.items():
            classes.sort(key = lambda x: x.getTStart())

    def getName(self):
        return self.__name

    def getClasses(self):
        return self.__classes
    
    def appendClass(self, c):
        self.__classes.append(c)
        self.classesByDOW()

    def __str__(self) -> str:
        return self.__name