from Course import Course

class Student:
    def __init__(self, name) -> None:
        self.name = name
        self.courses = []
        self.dowCourses = {}

    def coursesByDOW(self):
        # dict structure to split classes up by DOW
        for dow in range(0, 5):
            self.dowCourses[dow] = []

        for course in self.courses:
            dowList = course.dow
            # if class is not remote/async
            if course.dow is not None:
                for dow in course.dow:
                    self.dowCourses[dow].append(course)
                    
        # sort by time to create ordered widgets
        for dow, courses in self.dowCourses.items():
            courses.sort(key = lambda x: x.tStart)

    def __str__(self) -> str:
        return self.name