class Event():
    def __init__(self, name, tStart, tEnd, dStart, dEnd, loc = None) -> None:
        self.name = name
        self.tStart = tStart
        self.tEnd = tEnd
        self.dStart = dStart
        self.dEnd = dEnd
        self.loc = loc

    def formatTime(self, time, displayPeriod: bool = True):
        if displayPeriod:
            return time.strftime("%I:%M %p")
        else:
            return time.strftime("%I:%M")
            
    def __str__(self) -> str:
        return self.name
