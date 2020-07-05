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


users = []

@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == "POST":
		username = request.form.get('username')
		session["user"] = username
		return redirect("/chat")
	else:
		if session.get("user"):
			return redirect('/chat')
		return render_template("index.html")	

@app.route("/chat")
def chat():
	if session.get("user"):
		name = session["user"]
		return render_template("chat.html", username=name)	

