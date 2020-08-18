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

@socketio.on("reload user")
def reload_user(data):
	username = data["username"]
	channel_name = data["channel_name"]
	list_channels = list(messages.keys())
	emit("rejoin", {"list_channels":list_channels, "username": username, "channel_name":channel_name})


@socketio.on("add channel")
def add_channel(data):
	print("entered add channel function")
	channel_name = data["channel_name"]
	created_by = data["username"]
	if channel_name not in messages:
		messages[channel_name] = {
			"messages":[], 
			"users":set()}
		#print(type(messages[channel_name]["messages"]))	
		#print(type(messages))
		emit("available channels", {"list_channels": list(messages), "messages": messages[channel_name]["messages"], "username":created_by}, broadcast=True)
		#print(messages[channel_name])
		#print(messages)
		#print(channel)
		#channels.append(channel)
	#messages[channel] = []
	
	#emit("announce channel", {"channel_name" : channel_name}, broadcast=True)

@socketio.on("load data")
def load_data(data):
	list_channels = list(messages.keys())
	username = data["username"]
	print(list_channels)
	emit("available channels", {"list_channels":list_channels, "username":username})

@socketio.on('join channel')
def join_channel(data):
	print('entered the function')
	channel_name = data['channel_name']
	print(channel_name)
	username = data['username']
	timestamp = time.time()
	messages[channel_name]["users"].add(username)
	messages[channel_name]["messages"].append({
		"messages": "user has joined the channel",
		"username": username,
		"ts": timestamp
		})
	messages_list = messages[channel_name]["messages"]
	join_message = messages_list[-1]["messages"]
	if len(messages_list) > 100:
		messages_list.pop(0)
		print("popped off the first elem")
	 
	emit("user joined", {'username':username, "channel_name":channel_name, "messages": messages_list, "timestamp":timestamp, "join_message":join_message})

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
	if len(messages[channel_name]["messages"]) > 100:
		messages[channel_name]["messages"].pop(0)
		print("popped off the first elem")
	print(messages[channel_name])
	emit("send message", {'username':username, 'message': message, 'timestamp':timestamp, 'channel_name':channel_name}, broadcast=True)









