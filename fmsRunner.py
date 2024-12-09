from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for, jsonify, make_response
from os import listdir
import os
import random
import time
import json
import datetime
import pandas as pd
import csv
app = Flask(__name__)
thisClock = 0
users = ["bMedina", "rWelbourn", "root"]
passwords = ["graciousProffesionalism", "fll", "root"]
global matchNumber
matchNumber = 0
global blueTeam
blueTeam = 0
global redTeam
redTeam = 0
@app.route("/openCeremonies")
def opening():
    return render_template("openingTeleprompter.html")
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
    match1 = open("currentMatch.txt")
    for line3 in match1:
        thisMatch = line3
    match1.close()
    return render_template("redScorekeeper.html", match = thisMatch, teamNo = redTeam)
@app.route("/fta-blueScore", methods=["GET", "POST"])
def scoreBlue():
    match1 = open("currentMatch.txt")
    for line3 in match1:
        thisMatch = line3
    match1.close()
    return render_template("blueScorekeeper.html", match = thisMatch, teamNo = blueTeam)
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
@app.route('/controlPanel')
def controller():
    return render_template("controlPanel.html")
@app.route('/test1', methods=["GET"])
def test1():
        current = open("currentStatus.txt")
        #with open("currentStatus.txt", "w") as current:
        for line in current:
            thisStatus = line
        current.close()
        macro = open("macroStatus.txt")
        for line2 in macro:
            thisTest = line2[1]
            thisMacro = line2
        event1 = open("currentMatch.txt")
        for line1 in event1:
            thisMatch = line1
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "eventSchedule.json")
        eventJson = json.load(open(json_url))
        thisMatchData = eventJson["QT Bend"][int(thisMatch)+1]
        if(thisTest == "1" or thisTest == "2"):
            thisRed = "Test 1"
            thisBlue = "Test 2"
            thisTicker = "FMS Field Test"
            thisType = "FMS-TEST"
        else:
            thisRed = thisMatchData["teamR"]
            thisBlue = thisMatchData["teamB"]
            thisTicker = thisMatchData["activity"]
            thisType = thisMatchData["type"]
        clock = open("clockStatus.txt")
        for line2 in clock:
            thisClock = line2
        '''with open("clockStatus.txt", "w") as clockStatus1:
            if(thisClock == 1):
                clockStatus1.write(0)
                clockStatus1.close()'''
        return jsonify(thisStatus, thisRed, thisBlue, thisClock, thisType, thisTicker, thisMacro, thisTest, thisMatch)
@app.route('/test2', methods=["GET"])
def test2():
        cinema1 = open("redScore.txt")
        #with open("currentStatus.txt", "w") as current:
        for line in cinema1:
            thisRed = line
        cinema1.close()
        blue1 = open("blueScore.txt")
        for line2 in blue1:
            thisBlue = line2
        blue1.close()
        #return jsonify(thisCinema[0], thisCinema[1], thisCinema[2], thisCinema[3], thisCinema[4], thisCinema[5], thisCinema[6], thisCinema[7], thisCinema[8], thisCinema[9], thisCinema[10], thisCinema[11], thisCinema[12], thisCinema[13], thisCinema[14], thisCinema[15], thisCinema[16], thisCinema[17], thisCinema[18], thisCinema[19], thisCinema[20], thisCinema[21], thisCinema[22], thisBlue[0], thisBlue[1], thisBlue[2], thisBlue[3], thisBlue[4], thisBlue[5], thisBlue[6], thisBlue[7], thisBlue[8], thisBlue[9], thisBlue[10], thisBlue[11], thisBlue[12], thisBlue[13], thisBlue[14], thisBlue[15], thisBlue[16], thisBlue[17], thisBlue[18], thisBlue[19], thisBlue[20], thisBlue[21], thisBlue[22])
        return jsonify(thisRed, thisBlue)
@app.route('/test3', methods=["GET"])
def test3():
    red1 = open("redFinalStatus.txt")
    for line in red1:
        thisStatus = line
    red1.close()
    blue2 = open("blueFinal.txt")
    for line3 in blue2:
        thisStatus1 = line3
    blue2.close()
    return jsonify(thisStatus[0], thisStatus[1], thisStatus1[0], thisStatus1[1])
@app.route('/test5', methods=["GET"])
def test5():
    fullStatus = open("matchStatus.txt")
    for line in fullStatus:
        thisMatchStatus = line
    fullStatus.close()
    return jsonify(thisMatchStatus)
@app.route('/test6', methods=["GET", "POST"])
def submitMatchData():
    if request.method == "POST":
        blueRow = request.form["blue-final-data"]
    thisMatchData = blueRow
    thisMatchDataSplit = thisMatchData.split(",")
    with open('blueData.csv', 'a') as bd:
        writer = csv.writer(bd)
        writer.writerow(thisMatchDataSplit)
    return render_template("matchSubmitSuccessBlue.html", match = thisMatchDataSplit[0])
@app.route('/test7', methods=["GET", "POST"])
def submitMatchDataRed():
    if request.method == "POST":
        redRow = request.form["red-final-data"]
    thisMatchData = redRow
    thisMatchDataSplit = thisMatchData.split(",")
    with open('redData.csv', 'a') as rd:
        writer = csv.writer(rd)
        writer.writerow(thisMatchDataSplit)
    return render_template("matchSubmitSuccessRed.html", match = thisMatchDataSplit[0])
@app.route('/getmethod/<jsdata>/<eventdata>/<clock>/<status1>')
def get_javascript_data(jsdata, eventdata, clock, status1):
    with open("currentStatus.txt", "w") as status:
        status.write(jsdata)
        status.close()
    with open("currentMatch.txt", "w") as currentEvent:
        currentEvent.write(eventdata)
        currentEvent.close()
    with open("clockStatus.txt", "w") as clockStatus:
        clockStatus.write(clock)
        clockStatus.close()
    with open("matchStatus.txt", "w") as matchStatus:
        matchStatus.write(status1)
        matchStatus.close()
    return jsonify(result=jsdata)
@app.route('/getmethodred/<ready>/<datum>/<final>/<gp>')
def get_javascript_data_red(ready, datum, final, gp):
    with open("redScore.txt", "w") as cinemaStatus:
        cinemaStatus.write(datum)
        cinemaStatus.close()
    with open("redFinalStatus.txt", "w") as redFinal:
        redFinal.write(ready+final)
        redFinal.close()
    return jsonify(result=datum)
@app.route('/getmethodblue/<ready>/<datum>/<final>/<gp>')
def get_javascript_data_blue(ready, datum, final, gp):
    with open("blueScore.txt", "w") as blueScore:
        blueScore.write(datum)
        blueScore.close()
    with open("blueFinal.txt", "w") as blueFinal:
        blueFinal.write(ready+final)
        blueFinal.close()
    return jsonify(result=datum)
@app.route('/runmacro/<toh>/<test>/<resync>')
def update_macros(toh, test, resync):
    macro = toh + test + resync
    with open("macroStatus.txt", "w") as macroStatus:
        macroStatus.write(macro)
        macroStatus.close()
    return jsonify(result=macro)
@app.route("/finalScores/<blueteam>/<redteam>/<bluepts>/<redpts>")
def returnResults(blueteam, redteam, bluepts, redpts):
    return render_template("finalScores.html", blueTeam = blueteam, redTeam = redteam, blueScore = bluepts, redScore = redpts)
if __name__=="__main__":
    Flask.run(app, debug=True, host='0.0.0.0', threaded=True, port="8000")
