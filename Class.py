class Class:
    def __init__(self, name, fullName, prof, dow, tStart, tEnd, dStart, dEnd, loc) -> None:
        self.__name = name
        self.__fullName = fullName
        self.__prof = prof
        self.__dow = dow
        self.__tStart = tStart
        self.__tEnd = tEnd
        self.__dStart = dStart
        self.__dEnd = dEnd
        self.__loc = loc
        self.__students = []
    
    def getClassObject(self):
        return self

    def getName(self):
        return self.__name

    def getDOW(self):
        return self.__dow

    def getTStart(self):
        return self.__tStart

    def appendStudent(self, s):
        self.__students.append(s)

    def __str__(self) -> str:
        return self.__name