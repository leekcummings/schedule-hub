import pandas as pd

from Course import Course

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

    cTime = pd.to_datetime(f"{hours}:{minutes}", format="%H:%M").time()
    return cTime

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