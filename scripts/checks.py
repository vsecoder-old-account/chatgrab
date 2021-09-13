import datetime, json

from models import db_session
from models.users import User

file = ''

db_session.global_init('database.db')

def get_users():
	session = db_session.create_session()
	user_all = session.query(User).all()
	users = []

	for user in user_all:
		user_as_dict = {
			"id": user.id,
			"name": user.name,
			"fullname": user.fullname,
			"username": user.username,
			"data": user.data,
			"work": user.work
		}
		users.append(user_as_dict)

	return users

def get_data():
	f = open(f'settings.json', "r")
	settings = json.loads(f.read())
	return settings

def check_pass(login, password):
	f = open(f'settings.json', "r")
	settings = json.loads(f.read())
	admin_password = settings["password"] # password

	if admin_password == password:
		return True

def update_settings(token, admin_id, password):
	f = open(f'settings.json', "w")
	f.write('''{
	"token": "''' + token + '''",
	"admin_id": "''' + admin_id + '''",
	"password": "''' + password + '''"
}''')

def get_num():
	session = db_session.create_session()
	user_all = session.query(User).all()
	users = 0

	for user in user_all:
		users += 1

	return users

def get_log_files():
	import os
	directory = 'logs/'
	files = os.listdir(directory)
	m = []
	for file in files:
		m.append({
			"name": file
		})
	return m

def get_log_file(file):
	try:
		f = open(f'logs/{file}', "r+")
		text = f.read()
		f.close()
		print(text)
		return text
	except Exception as e:
		print(e)
		return 'File not found'

def print_log(msg, status, app):
	text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}: - {app}:[{status}] - {msg}\n'

	try:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.txt', "a")
		f.write(text)
		f.close()
	except:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.txt', "w")
		f.write(text)
		f.close()
	print(text)

async def async_print_log(msg, status, app):
	text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}: - {app}:[{status}] - {msg}\n'

	try:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.txt', "a")
		f.write(text)
		f.close()
	except:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.txt', "w")
		f.write(text)
		f.close()
	print(text)