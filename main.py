from flask import Flask, render_template
from flask import request
from flask import Markup
from datetime import datetime
from datetime import timedelta
import csv
import databaseUtil

app = Flask(__name__)

#signifying two routes to the homepage so we can link to it and have it as the landing page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/booking')
def booking():
    bookList = databaseUtil.returnAllBookings()
    confirmedList = []
    for line in bookList:
        #print(line[6])
        if line[6] is "1":
            confirmedList.append(line)
    #you can pass functions to the web app to use in templates!
    return render_template('roomBooking.html', aList = confirmedList, getRoomType=databaseUtil.getRoomType)
    
@app.route('/bookroom', methods=['post'])
def bookroom():
    fName = request.form['fname']
    lName = request.form['lname']
    roomType = request.form['roomtype']
    email = request.form['email']
    sDate = request.form['arrive']
    eDate = request.form['depart']
    
	#checking all the inputs are filled and returning an error if not
    if not fName:
        error = Markup("<h2 class='error'> No first name entered! </h2>")
        return render_template('roomBooking.html', error = error)
    if not lName:
        error = Markup("<h2 class='error'> No last name entered! </h2>")
        return render_template('roomBooking.html', error = error)
    if not roomType:
        error = Markup("<h2 class='error'> No room type selected! </h2>")
        return render_template('roomBooking.html', error = error)
    if not email:
        error = Markup("<h2 class='error'> No email entered! </h2>")
        return render_template('roomBooking.html', error = error)
    if not sDate:
        error = Markup("<h2 class='error'> No start date selected! </h2>")
        return render_template('roomBooking.html', error = error)
    if not eDate:
        error = Markup("<h2 class='error'> No end date Selected! </h2>")
        return render_template('roomBooking.html', error = error)
    
	#check if the dates are valid
    if databaseUtil.compareDates(sDate, eDate):
        error = Markup("<h2 class='error'> The dates entered are not valid! </h2>")
        return render_template('roomBooking.html', error = error)
	#check if the start date is in the future
    if datetime.strptime(sDate, '%Y-%m-%d') < datetime.today():
        error = Markup("<h2 class='error'> Must choose date in the future! </h2>")
        return render_template('roomBooking.html', error = error)
    
	#check if a similar booking is already in the system
    getBookingFromDB = databaseUtil.returnBooking(email, sDate, eDate)
    if getBookingFromDB:
        error = Markup("<h2 class='error'> You've already booked on this date, please contact us to book more than one room. </h2>")
        return render_template('roomBooking.html', error = error)

    #write booking, retrieve booking, show booking conformation page
    databaseUtil.writeBooking(fName, lName, sDate, eDate, roomType, email)
    getBookingFromDB = databaseUtil.returnBooking(email, sDate, eDate)
    roomTypeString = databaseUtil.getRoomType(roomType)
    daysStaying = databaseUtil.deltaDays(sDate, eDate)
    price = databaseUtil.stayPrice(daysStaying, roomType)
    return render_template('confirmbooking.html', alist = getBookingFromDB, roomType = roomTypeString, deltaDays = daysStaying, price = price)
    
@app.route('/review')
def review():
    listComments = databaseUtil.returnComments()
    return render_template('comments.html', aList=listComments)
    
@app.route('/addComment', methods=['post'])
def addComment():
    name = request.form['name']
    content = request.form['comment']
    rating = request.form['rating']
    
	#checking all the inputs and returning an error if they are not
    if not name:
        listComments = databaseUtil.returnComments()
        error = Markup("<h2 class='error'> No Name Entered! </h2>")
        return render_template('comments.html', error = error, aList=listComments)
    if not content:
        listComments = databaseUtil.returnComments()
        error = Markup("<h2 class='error'> No Comment Entered! </h2>")
        return render_template('comments.html', error = error, aList=listComments)
    if not rating:
        listComments = databaseUtil.returnComments()
        error = Markup("<h2 class='error'> No Rating Given! </h2>")
        return render_template('comments.html', error = error, aList=listComments)
    
    databaseUtil.writeComments(name, content, rating)
    listComments = databaseUtil.returnComments()
    return render_template('comments.html', aList=listComments)
    
@app.route('/contact')
def contact():
    return render_template('contact.html')
	
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')
	
@app.route('/attractions')
def attractions():
    return render_template('localattractions.html')
    
if __name__=='__main__' :
    app.run(debug=True)