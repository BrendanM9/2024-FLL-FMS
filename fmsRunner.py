from flask import Flask, render_template, request, Response, stream_with_context, redirect, url_for, jsonify
from os import listdir
import random
import time
import json
import datetime
app = Flask(__name__)
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
        return jsonify(thisStatus)
@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    with open("currentStatus.txt", "w") as status:
        status.write(jsdata)
        status.close()
    return jsonify(result=jsdata)
if __name__=="__main__":
    Flask.run(app, debug=True, host='127.0.0.1', threaded=True)