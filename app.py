from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, send_file
from cfApi import *
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_ngrok import run_with_ngrok


interfaces = [
	'name',
	'other',
	'description',
	'urls',
	'paste',
	'user'
]
app = Flask(__name__)
# run_with_ngrok(app)
app.config['SECRET_KEY'] = generate_password_hash('Alfred Hitchcock')
app.config['SQLALCHEMY_DATABASE_URI'] = 'C:\project-algoblog\app.py'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Algo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	other = db.Column(db.String, nullable=False)
	description = db.Column(db.Text, nullable=False)
	urls = db.Column(db.Text, nullable=False)
	paste = db.Column(db.String, unique=True, nullable=False)
	assert isinstance(db.String, object)
	user = db.Column(db.String, nullable=False)


def updateDB():
	A = Algo()
	A.name = session['algo']['name']
	A.other = session['algo']['other']
	A.description = session['algo']['description']
	A.urls = session['algo']['urls']
	A.paste = session['algo']['paste']
	A.user = session['algo']['user']
	db.session.add(A)
	db.session.commit()


def changeDB(note):
	db.session.merge(note)
	db.session.commit()


def deleteDB(note):
	db.session.delete(note)
	db.session.commit()


@app.route('/')
def index():
	kwargs = dict()
	kwargs['title'] = 'Home'
	kwargs['content_title'] = 'Home'
	return render_template('index.html', **kwargs, **session)


@app.route('/algo/adding/', methods=['post', 'get'])
def adding():
	kwargs = dict()
	kwargs['title'] = 'Adding'
	kwargs['content_title'] = 'Adding'
	if not session.get('user'):
		session['message'] = 'Уважаемый аноним, залогиньтесь!'
		return redirect('/message')
	if request.method == 'POST':
		session['algo'] = session.get('algo', dict())
		name = request.form.get('name')
		other = request.form.get('other')
		description = request.form.get('description')
		urls = request.form.get('urls')
		paste = request.form.get('paste')
		user = session.get('user')
		if name:
			session['algo']['name'] = name
		if other:
			session['algo']['other'] = other
		if description:
			session['algo']['description'] = description
		if urls:
			session['algo']['urls'] = urls
		if paste:
			session['algo']['paste'] = paste
		session['algo']['user'] = user['handle']
		if (all([session['algo'].get(i) for i in interfaces])):
			updateDB()
			session.pop('algo')
			return redirect('/algo')
	return render_template('adding.html', **kwargs, **session)


@app.route('/algo/', methods=['post', 'get'])
def algo():
	kwargs = dict()
	kwargs['title'] = 'Algo'
	kwargs['content_title'] = 'Algo'
	session.pop('algo') if session.get('algo') else None
	if request.method == 'POST' and session.get('auth'):
		return redirect('/algo/adding')
	data = reversed(Algo.query.all())
	flt = request.args.get('search', '')
	if not flt or flt[0] != '@':
		data = filter(lambda x: searchFunc(x, flt), data)
	else:
		data = filter(lambda x: authorFunc(x, flt[1:]), data)
	return render_template('algo.html', **kwargs, **session, data=data)


@app.route('/login/', methods=['post', 'get'])
def login():
	kwargs = dict()
	kwargs['title'] = 'Login'
	kwargs['content_title'] = 'Login'
	kwargs['sendMail'] = sendMail
	if request.method == 'POST':
		handle = request.form.get('handle')
		code = request.form.get('code')
		if handle:
			session['handle'] = handle
			session['user'] = userInfo(handle)
			session['color'] = getColor(session['user'])
			session['email'] = session['user'].get('email') if session['user'] else None
			session['secret'] = str(randint(1000, 9999))
			session['auth'] = False
		session['code'] = code if code else str()
		if session['code'] and session['secret'] and session['code'] == session['secret']:
			session['auth'] = True
	return render_template('login.html', **kwargs, **session)


@app.route('/logout/')
def logout():
	kwargs = dict()
	kwargs['title'] = 'Logout'
	kwargs['content_title'] = 'Logout'
	session.clear()
	# session.pop('email') if session.get('email') else None
	# session.pop('code') if session.get('code') else None
	# session.pop('handle') if session.get('handle') else None
	# session.pop('secret') if session.get('secret') else None
	# session.pop('auth') if session.get('auth') else None
	return render_template('logout.html', **kwargs, **session)


@app.route('/reading/<id>/')
def reading(id):
	kwargs = dict()
	ans = Algo.query.filter(Algo.id == int(id))[0]
	kwargs['title'] = ans.name
	kwargs['content_title'] = ans.name
	kwargs['getTitle'] = getTitle
	return render_template('reading.html', **kwargs, **session, note=ans)


@app.route('/edit/<id>/', methods=['post', 'get'])
def edit(id):
	kwargs = dict()
	kwargs['title'] = 'Edit'
	kwargs['content_title'] = 'Edit'
	note = Algo.query.filter(Algo.id == int(id))[0]
	kwargs['algo'] = dict()
	kwargs['algo']['name'] = note.name
	kwargs['algo']['other'] = note.other
	kwargs['algo']['description'] = note.description
	kwargs['algo']['urls'] = note.urls
	kwargs['algo']['paste'] = note.paste
	if not session.get('auth'):
		session['message'] = 'Уважаемый аноним, залогиньтесь!'
		return redirect('/message')
	if not session.get('user') or session['user']['handle'] != note.user:
		session['message'] = 'Вы не являетесь автором этой записи!'
		return redirect('/message')
	if request.method == 'POST':
		session['algo'] = session.get('algo', dict())
		name = request.form.get('name')
		other = request.form.get('other')
		description = request.form.get('description')
		urls = request.form.get('urls')
		paste = request.form.get('paste')
		user = session.get('user')
		if name:
			session['algo']['name'] = name
		if other:
			session['algo']['other'] = other
		if description:
			session['algo']['description'] = description
		if urls:
			session['algo']['urls'] = urls
		if paste:
			session['algo']['paste'] = paste
		session['algo']['user'] = user['handle']
		if (all([session['algo'].get(i) for i in interfaces])):
			session['algo']['name'] = note.name = name
			session['algo']['other'] = note.other = other
			session['algo']['description'] = note.description = description
			session['algo']['urls'] = note.urls = urls
			session['algo']['paste'] = note.paste = paste
			changeDB(note)
			session.pop('algo')
			return redirect('/algo')
	kwargs.pop('algo') if session.get('algo') else None
	return render_template('adding.html', **kwargs, **session, note=note)


@app.route('/delete/<id>/')
def delete(id):
	note = Algo.query.filter(Algo.id == int(id))[0]
	if not session.get('auth'):
		session['message'] = 'Уважаемый аноним, залогиньтесь!'
		return redirect('/message')
	if session.get('user')['handle'] == note.user:
		deleteDB(note)
		return redirect('/algo')
	session['message'] = 'Вы не являетесь автором этой записи!'
	return redirect('/message')


@app.route('/message/')
def message():
	kwargs = dict()
	kwargs['title'] = 'Message'
	kwargs['content_title'] = 'Message'
	return render_template('message.html', **kwargs, **session)


@app.route('/sponsors/')
def sponsors():
	kwargs = dict()
	kwargs['title'] = 'Sponsors'
	kwargs['content_title'] = 'Sponsors'
	return render_template('sponsors.html', **kwargs, **session)


@app.route('/downloads/')
def downloads():
	kwargs = dict()
	kwargs['title'] = 'Downloads'
	kwargs['content_title'] = 'Downloads'
	return render_template('downloads.html', **kwargs, **session)


@app.route('/downloads/<name>/')
def download(name):
	#return name
	return send_file('static/code/make.py', as_attachment=True)


if __name__ == '__main__':
	app.run(debug=True)