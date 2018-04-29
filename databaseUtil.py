import csv
import time
from datetime import datetime
from datetime import timedelta

def read(aFile):
    with open(aFile, 'r') as inFile:
        reader = csv.reader(inFile)
        aList = [row for row in reader]
    return aList

def write(aList, aFile):
    originalList = read(aFile)
    print(originalList)
    print(aList)
    originalList.append(aList)
    with open(aFile, 'w', newline='') as outFile:
        writer = csv.writer(outFile)
        for row in originalList:
            writer.writerow(row)

def writeBooking(fName, lName, sDate, eDate, roomType, email):
    aFile = "static/db/roombookings.csv"
    confirmed = 0
    dateTimeRequested = datetime.today().strftime('%d-%m-%Y %H:%M')
    aList = [fName, lName, sDate, eDate, roomType, email, confirmed, dateTimeRequested]
    write(aList, aFile)

def returnBooking(emailAd, sDate, eDate):
    returnedList = returnAllBookings()
    for element in returnedList:
        if emailAd == element[5] and sDate == element[2] and eDate == element[3]:
            return element

def returnAllBookings():
    aFile = "static/db/roombookings.csv"
    returnedList = read(aFile)
    return returnedList

def returnComments():
    aFile = "static/db/comments.csv"
    returnedList = read(aFile)
    return returnedList
    
def writeComments(name, content, stars):
    aFile = "static/db/comments.csv"
    aList = [name, content, stars, datetime.today().strftime('%d-%m-%Y %H:%M')]
    write(aList, aFile)

def compareDates(dateA, dateB):
    dateAObject = datetime.strptime(dateA, '%Y-%m-%d')
    dateBObject = datetime.strptime(dateB, '%Y-%m-%d')
    dateDelta = dateBObject - dateAObject
    if dateDelta > timedelta(0):
        return False
    else:
        return True
        
def deltaDays(dateA, dateB):
    dateAObject = datetime.strptime(dateA, '%Y-%m-%d')
    dateBObject = datetime.strptime(dateB, '%Y-%m-%d')
    dateDelta = dateBObject - dateAObject
    return dateDelta.days
    
def getRoomType(roomTypeID):
    aFile = "static/db/rooms.csv"
    roomList = read(aFile)
    for rooms in roomList:
        if int(rooms[0]) is int(roomTypeID):
            return rooms[1]
    return "none"

def stayPrice(days, roomType):
    aFile = "static/db/rooms.csv"
    roomList = read(aFile)
    for rooms in roomList:
        if int(rooms[0]) is int(roomType):
            roomPrice = int(rooms[2])
    return roomPrice * int(days)