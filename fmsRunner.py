from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for, jsonify
from os import listdir
import os
import random
import time
import json
import datetime
app = Flask(__name__)
thisClock = 0
users = ["bMedina", "rWelbourn"]
passwords = ["graciousProffesionalism", "fll"]
@app.route("/")
def fmsHome():
    return render_template("home.html")
@app.route("/create")
def newEvent():
    return render_template("newTournament.html", methods=["GET", "POST"])
@app.route("/submitNew")
def submit():
    return render_template("newTournament.html")
@app.route("/newTournamentConfirmation", methods=["GET", "POST"])
def updateEvents():
    if request.method == "POST":
        thisLocation = request.form["location"]
        thisStartDate = request.form.get("startDate")
        thisEndDate = request.form.get("endDate")
    eventLog = open("eventList.txt")
    locations = []
    startDates = []
    endDates = []
    for line in eventLog:
        location = ""
        startDate = ""
        endDate = ""
        index = 0
        while (line[index] != ","):
            location = location + line[index]
            index = index + 1
        index = index + 1
        while (line[index] != "-"):
            startDate = startDate + line[index]
            index = index + 1
        index = index + 1
        while (line[index] != "\n"):
            endDate = endDate + line[index]
            index = index + 1
        locations.append(location)
        startDates.append(startDate)
        endDates.append(endDate)
    index1 = len(locations) + 1
    locations.insert(index1, thisLocation)
    startDates.insert(index1, thisStartDate)
    endDates.insert(index1, thisEndDate)
    with open("eventList.txt", "w") as f:
        for index2 in range(len(locations)):
            f.write(str(locations[index2]) + "," + str(startDates[index2]) + "-" + str(endDates[index2])+ "\n")
    eventLog.close()
    print(locations)
    print(startDates)
    print(endDates)
    return render_template("tournamentCreateSuccess.html", thisLocation = thisLocation, thisStartDate = thisStartDate, thisEndDate = thisEndDate)
@app.route("/ftaHome", methods=["GET", "POST"])
def ftaHome():
    loginStatus = ""
    if request.method == "POST":
        user = request.form["username"]
        password = request.form.get("password")
        if user in users:
            if password in passwords:
                loginStatus = render_template("ftaHome.html")
            else:
                loginStatus = "Incorrect Password"
        else:
            loginStatus = "Incorrect Username"
    else:
        loginStatus = "NO"
    return loginStatus
@app.route("/fta-audienceDisplaySet", methods=["GET", "POST"])
def setAudienceDisplay():
    '''if request.headers.get('accept') == 'text/event-stream':
        def getRandom():
            while True:
                yield "Hello, World!"
                time.sleep(1)
        return Response(getRandom(), content_type='text/event-stream')
    return redirect(url_for('127.0.0.1:5000/audience'))'''
    return render_template("setAudienceDisplay.html")
@app.route("/fta-redScore", methods=["GET", "POST"])
def scoreRed():
    return render_template("redScorekeeper.html")
@app.route("/fieldLogin")
def ftaLogin():
    return render_template("fieldLogin.html")
@app.route("/audience", methods=["GET", "POST"])
def showDisplay():
    thisMatch = 1
    totalMatches = 15
    redTeam = "Test 1"
    redScore = 00
    redBonus = ""
    #currentStatus = "Match Under Review"
    #currentStatus = "Match Being Scored"
    #currentStatus = "Match In Progress"
    #currentStatus = "Match Queueing"
    #currentStatus = "Break, Will Return:"
    #currentStatus = "No Match Set"
    #currentStatus = "Match Scored"
    #currentStatus = "Match Starting"
    #currentStatus = "Practice Match"
    currentStatus = "FMS-TEST"
    blueTeam = "Test 2"
    blueScore = 00
    blueBonus = ""
    return render_template("audienceDisplay.html", thisMatch = thisMatch, totalMatches = totalMatches, redTeam= redTeam, redScore = redScore, redBonus = redBonus, currentStatus = currentStatus, blueTeam = blueTeam, blueScore = blueScore, blueBonus = blueBonus)
@app.route('/test1', methods=["GET"])
def test1():
        current = open("currentStatus.txt")
        #with open("currentStatus.txt", "w") as current:
        for line in current:
            thisStatus = line
        current.close()
        event1 = open("currentMatch.txt")
        for line1 in event1:
            thisMatch = line1
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "eventSchedule.json")
        eventJson = json.load(open(json_url))
        thisMatchData = eventJson["QT Bend"][int(thisMatch)+1]
        if(thisStatus != "FMS-TEST"):
            thisRed = thisMatchData["teamR"]
            thisBlue = thisMatchData["teamB"]
            thisTicker = thisMatchData["activity"]
            thisType = thisMatchData["type"]
        else:
            thisRed = "Test 1"
            thisBlue = "Test 2"
            thisTicker = "FMS Field Test"
            thisType = "FMS-TEST"
        clock = open("clockStatus.txt")
        for line2 in clock:
            thisClock = line2
        '''with open("clockStatus.txt", "w") as clockStatus1:
            if(thisClock == 1):
                clockStatus1.write(0)
                clockStatus1.close()'''
        return jsonify(thisStatus, thisRed, thisBlue, thisClock, thisType, thisTicker)
@app.route('/test2', methods=["GET"])
def test2():
        cinema1 = open("cinema.txt")
        #with open("currentStatus.txt", "w") as current:
        for line in cinema1:
            thisCinema = line
        cinema1.close()
        return jsonify(thisCinema)

@app.route('/getmethod/<jsdata>/<eventdata>/<clock>')
def get_javascript_data(jsdata, eventdata, clock):
    with open("currentStatus.txt", "w") as status:
        status.write(jsdata)
        status.close()
    with open("currentMatch.txt", "w") as currentEvent:
        currentEvent.write(eventdata)
        currentEvent.close()
    with open("clockStatus.txt", "w") as clockStatus:
        clockStatus.write(clock)
        clockStatus.close()
    return jsonify(result=jsdata)
@app.route('/getmethodred/<cinema>')
def get_javascript_data_red(cinema):
    with open("cinema.txt", "w") as cinemaStatus:
        cinemaStatus.write(cinema)
        cinemaStatus.close()
    return jsonify(result=cinema)
if __name__=="__main__":
    Flask.run(app, debug=True, host='0.0.0.0', threaded=True)