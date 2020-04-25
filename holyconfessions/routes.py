from flask import render_template, url_for, flash, redirect, Response
from holyconfessions import app, bcrypt
from holyconfessions.forms import RegistrationForm, LoginForm
from holyconfessions.models import User, Post
from flask_login import login_user, current_user, logout_user
from holyconfessions import db

import random
import time
import json
from datetime import datetime


posts = [
	{
		'author': 'Doruk',
		'title': 'Olumsuzluk',
		'date': '22.04.1998'
	},
	{
		'author': 'Doruk',
		'title': 'Motorsiklet',
		'date': '20.05.2019'
	}
	
]


labels = [
	'JAN', 'FEB', 'MAR', 'APR',
	'MAY', 'JUN', 'JUL', 'AUG',
	'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
	967.67, 1190.89, 1079.75, 1349.19,
	2328.91, 2504.28, 2873.83, 4764.87,
	4349.29, 6458.30, 9907, 16297
]





@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('{} adli hesap olusturuldu.'.format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Giris basarisiz.', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))



# This is a self-reloading example without <meta http-equiv="refresh" content="5">
@app.route('/dashboard')
def dashboard():
	def generate_random_data():
		while True:
			json_data = json.dumps(
				{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
			yield f"data:{json_data}\n\n"
			time.sleep(1)

	return Response(generate_random_data(), mimetype='text/event-stream')




@app.route('/bar')
def bar():
	labels.append('TEST')
	values.append(100)
	return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=labels, values=values)




