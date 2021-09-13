from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
import os, string, random, time
from scripts.checks import update_settings, get_data, get_users, get_num, print_log, get_log_files, get_log_file, check_pass
from bot import ad_send
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEY'

ADMINS = []

@app.route("/", methods=['GET', 'POST'])
def index():
	users = get_num()
	print_log(f"Page: \"/\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True

	return render_template('index.html', users=users, authenticated=authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	print_log(f"Page: \"/login\" | {request.remote_addr}", 'INFO', 'WEB')
	login = request.form.get('user')
	password = request.form.get('pass')

	if login and password:
		user = check_pass(login, password)

		if user:
			ADMINS.append(request.remote_addr)
			print_log(f"Admin login: {request.remote_addr}", 'INFO', 'WEB')

			return redirect('/')
		else:
			flash('Не верны Логин/Пароль')
	else:
		pass
	return render_template('login.html')

@app.route("/users", methods=['GET', 'POST'])
def index1():
	u = get_users()
	print_log(f"Page: \"/users\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	return render_template('users.html', users=u, authenticated=authenticated)

@app.route("/user/<id>", methods=['GET', 'POST'])
def index2(id):
	print_log(f"Page: \"/user/{id}\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	return render_template('user.html', id=id, authenticated=authenticated)

@app.route("/ad", methods=['GET', 'POST'])
def index3():
	print_log(f"Page: \"/ad\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	return render_template('ad.html', authenticated=authenticated)

@app.route("/settings", methods=['GET', 'POST'])
def index7():
	print_log(f"Page: \"/settings\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	data = get_data()
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	token = request.form.get('token')
	adminid = request.form.get('adminid')
	password = request.form.get('password')
	if token and adminid and password:
		update_settings(token, adminid, password)
		return redirect('/')
	else:
		return render_template('settings.html', authenticated=authenticated, data=data)

@app.route("/send", methods=['GET', 'POST'])
def index4():
	text = ''
	if request.method == 'GET':
		text = request.values.get('text')
	elif request.method == 'POST':
		text = request.form.get('text')
	print_log(f"Page: \"/send\" | {request.remote_addr}", 'INFO', 'WEB')
	ioloop = asyncio.new_event_loop()
	ioloop.run_until_complete(ad_send(text))
	ioloop.close()
	return jsonify({'Кол-во получателей смотрите в логах': ''})

@app.route("/logs", methods=['GET', 'POST'])
def index5():
	files = get_log_files()
	print_log(f"Page: \"/logs\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	return render_template('logs.html', files=files, authenticated=authenticated)

@app.route("/log/<file>", methods=['GET', 'POST'])
def index6(file):
	text = get_log_file(file)
	print_log(f"Page: \"/logs\" | {request.remote_addr}", 'INFO', 'WEB')
	authenticated = False
	for admin in ADMINS:
		if request.remote_addr == admin:
			authenticated = True
	return render_template('log.html', file=text, authenticated=authenticated)

@app.errorhandler(404)
def not_found_error(error):
	print_log(f"404", 'WARNING', 'WEB')
	return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
	print_log(f"500", 'ERROR', 'WEB')
	return render_template('500.html'), 500

if __name__ != '__main__':
	print_log(f"Web starting in 0.0.0.0:5000", 'INFO', 'WEB')
	port = int(os.environ.get("PORT", 3000))
	app.run(host='0.0.0.0', port=port)
	print_log(f"Web stoping", 'INFO', 'WEB')