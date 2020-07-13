import os
from flask import Flask, session, render_template, url_for, request, redirect, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bootstrap import Bootstrap



app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
bootstrap = Bootstrap(app)
socketio = SocketIO(app)
Session(app)

#dictionary of users and channels
users = []
channels = []


@app.route("/")
def index():
	return render_template("index.html")

@socketio.on("add user")
def add_user(data):
	username = data["username"]
	if username not in users:
		users.append(username)
		
	print(users)	



