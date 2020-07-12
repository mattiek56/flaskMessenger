import os
from flask import Flask, session, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap



app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
bootstrap = Bootstrap(app)
Session(app)

#dictionary of users and channels
users = []
channels = []


@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == "POST":
		username = request.form.get('username')
		#add user to the list of users
	
		if username not in users:	
			users.append(username)
		return redirect("/home")
	else:
		return render_template("index.html")	


@app.route("/home", methods=["POST", "GET"])
def home():
		
	if request.method == "GET":
		channels_list = channels
		return render_template("home.html", channels = channels_list)

	else:
		new_channel = request.form.get('channel-name')
		#check if the channel exists (need to add in not letting a creation happen if there is no value)
		if new_channel not in channels:
			channels.append(new_channel)
			channels_updated = channels
			return render_template("home.html", channels = channels_updated)
		else: 
			channels_list = channels
			return render_template("home.html", channels = channels_list, error='This channel already exists')




