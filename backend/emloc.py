from flask import Flask, session, redirect, url_for, escape, request, jsonify, g

import sqlite3

app = Flask(__name__)

DATABASE = 'db'

def connect_db():
	return sqlite3.connect(DATABASE)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_db()
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	get_db().commit()
	rv = [dict((cur.description[idx][0], value)
			for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('create_db.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

class Node:
	def __init__(self, secret):
		self.secret = secret
		self.location = {"lat":0, "lon":0}

	def setLocation(self, lat, lon):
		self.location["lat"] = lat
		self.location["lon"] = lon

def findNode(secret):
	for node in nodes:
		if node.secret == secret:
			return node
	return null

@app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		if request.form['request'] == "REGISTER":
			name = request.form['name']
			lat = request.form['lat']
			lon = request.form['lon']
			query = """INSERT INTO nodes(name, lat, lon)
			values (?, ?, ?)"""

			query_db(query, (name, lat, lon))
	return 'woo'

@app.route('/loc', methods=['POST'])
def loc():
	if request.method == 'POST':
		node = findNode(request.form['secret'])
		if node:
			node.lat = request.form['lat']
			node.lon = request.form['lon']

@app.route('/freq', methods=['GET','POST'])
def freq():
	if request.method == 'GET':
		return freq
	if request.method == 'POST':
		if request.form['freq']:
			freq = request.form['freq']

@app.route('/mode', methods=['GET','POST'])
def mode():
	if request.method == 'GET':
		return mode
	if request.method == 'POST':
		if request.form['mode']:
			mode = request.form['mode']

@app.route('/gain', methods=['GET','POST'])
def gain():
	if request.method == 'GET':
		return gain
	if request.method == 'POST':
		if request.form['gain']:
			gain = request.form['gain']

@app.route('/ping', methods=['GET'])
def ping():
	if request.method == 'GET':
		#return jsonify(frequency=freq, gain=gain, mode=mode)
		return "ok"

@app.errorhandler(500)
def internal_error(error):
	print error

init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0')

