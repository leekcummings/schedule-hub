from Class import Class

class Student:
    def __init__(self, name) -> None:
        self.__name = name
        self.__classes = []
        self.__currentClass = None
        self.__orderedClasses = {}

    def getOrderedClasses(self):
        for dow in range(0, 5):
            self.__orderedClasses[dow] = []
        for cName in self.__classes:
            cObject = cName.getClassObject()
            dowList = cObject.getDOW()
            if dowList is not None:
                for dow in dowList:
                    self.__orderedClasses[dow].append(cObject)
        for dow, classes in self.__orderedClasses.items():
            classes.sort(key = lambda x: x.getTStart())

    def getClasses(self):
        return self.__classes
    
    def appendClass(self, c):
        self.__classes.append(c)

    def __str__(self) -> str:
        return self.__name