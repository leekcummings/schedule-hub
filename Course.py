from Event import Event

class Course(Event):
    def __init__(self, name, fullName, prof, dow, tStart, tEnd, dStart, dEnd, loc) -> None:
        super().__init__(name, tStart, tEnd, dStart, dEnd)
        self.name = name
        self.fullName = fullName
        self.prof = prof
        self.dow = dow
        self.tStart = tStart
        self.tEnd = tEnd
        self.dStart = dStart
        self.dEnd = dEnd
        self.loc = loc
        self.students = []
    
    def getFullName(self):
        return self.fullName