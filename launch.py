import os
import re
import pandas as pd

def fileCheck():
    path = os.path.join(os.getcwd(), "spreadsheets")
    if "spreadsheets" not in os.listdir():
        # make dir to hold spreadsheets
        os.mkdir(path)
    if not os.listdir(path):
        # allow users to enter files at some point
        print("Please insert files into spreadsheet folder")
        exit()

def getStudentNameFromDF():
    students = {}
    # for spreadsheets in folder
    for f in os.listdir('./spreadsheets'):
        if re.search(r"\.xlsx", f):
            # get cd to find filepath
            cd = os.getcwd()
            # pull student name from spreadsheet
            name = pd.read_excel(cd+"/spreadsheets/"+f, skiprows=2).iat[0, 0].split(" (")[0]
            students[name] = pd.read_excel(cd+"/spreadsheets/"+f, skiprows=2)
        else:
            print(f"{f} could not be read (must be .xlsx file)")
    return students

def selectSelfName(studs):
    numStud = 0
    userInput = None
    studsSorted = sorted(studs.keys())
    print("Please type the number that corresponds with your name.")

    while userInput == None:
        for stud in studsSorted:
            numStud += 1
            print(f"{numStud}: {stud}")

        try:
            userInput = int(input(""))
        except:
            print("A valid input must be an integer.")

        if userInput not in range(1, numStud+1):
            userInput = None
            numStud = 0
        
    userName = studsSorted[userInput-1]

    return userName