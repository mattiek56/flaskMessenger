import os
from flask import Flask, session, render_template, url_for, request, redirect, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bootstrap import Bootstrap
import time



app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
bootstrap = Bootstrap(app)
socketio = SocketIO(app)
Session(app)

#dictionary of users and channels
users = []
messages = {}


@app.route("/")
def index():
	return render_template("index.html")

@socketio.on("add user")
def add_user(data):
	username = data["username"]
	if username not in users:
		users.append(username)
	emit('user load', {"username": username})

@socketio.on("add channel")
def add_channel(data):
	channel_name = data["channel_name"]
	if channel_name not in messages:
		messages[channel_name] = {
			"messages":["initialize messages"], 
			"users":set()}
		emit("announce channel", {"channel_name" : channel_name}, broadcast=True)
		#print(messages[channel_name])
		#print(messages)
		#print(channel)
		#channels.append(channel)
	#messages[channel] = []
	print(messages)
	#emit("announce channel", {"channel_name" : channel_name}, broadcast=True)

@socketio.on("load data")
def load_data(data):
	list_channels = list(messages.keys())
	print(list_channels)
	emit("available channels", {"list_channels":list_channels}, broadcast=True)

@socketio.on('join channel')
def join_channel(data):
	print('entered the function')
	channel_name = data['channel_name']
	username = data['username']
	timestamp = time.time()
	messages[channel_name]["users"].add(username)
	print(messages[channel_name])
	list_messages = messages[channel_name]["messages"]
	emit("load messages", {'username':username, "channel_name":channel_name, "timestamp":timestamp, "messages": list_messages}, broadcast=True)

@socketio.on("add message")
def add_message(data):
	print('adding the message')
	message = data['message']
	username = data['username']
	channel_name = data['channel_name']
	timestamp = data['timestamp']
	messages[channel_name]["messages"].append({
		"messages":message,
		"username": username,
		"ts":timestamp
	})


	emit("send message", {'username':username, 'message': message, 'timestamp':timestamp}, broadcast=True)









