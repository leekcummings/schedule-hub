class Course:
    def __init__(self, name, fullName, prof, dow, tStart, tEnd, dStart, dEnd, loc) -> None:
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
    
    def __str__(self) -> str:
        return self.name