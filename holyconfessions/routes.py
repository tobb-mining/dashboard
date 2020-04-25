from flask import render_template, url_for, flash, redirect, Response, request
from holyconfessions import app, bcrypt
from holyconfessions.forms import RegistrationForm, LoginForm, TagForm, SelectDimensionsForm
from holyconfessions.models import User, Post, Tag
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
	'OCA', 'ŞUB', 'MAR', 'NİS',
	'MAY', 'HAZ', 'TEM', 'AĞU',
	'EYL', 'EKİ', 'KAS', 'ARA'
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
@app.route('/stream')
def stream():
	def generate_random_data():
		while True:
			json_data = json.dumps(
				{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
			yield f"data:{json_data}\n\n"
			time.sleep(1)

	return Response(generate_random_data(), mimetype='text/event-stream')



@app.route('/submit_tag', methods=['GET', 'POST'])
def submit_tag():
	form = TagForm()
	if form.validate_on_submit():
		tag = Tag(username=current_user.usernamee, key=form.key.data, value=form.value.data)
		db.session.add(tag)
		db.session.commit()
		flash('{} adli tag olusturuldu.'.format(form.key.data), 'success')
		return redirect(url_for('tags'))
	return render_template('submit_tag.html', title='Submit Tag', form=form)	


@app.route('/tags', methods=['GET', 'POST'])
def tags():
	form = SelectDimensionsForm()
	user_tags = Tag.query.filter_by(username=current_user.usernamee)
	groups_list=[(tag.key, tag.key) for tag in user_tags]
	form.key1.choices = groups_list
	form.key2.choices = groups_list

	if form.validate_on_submit():
		tag1 = form.key1.data
		tag2 = form.key2.data
		return redirect(url_for('dashboard', tag1=tag1, tag2=tag2))

	my_tags = Tag.query.filter_by(username=current_user.usernamee)
	return render_template('select_tags.html', form=form)
	'''
	tags = []
	for tag in my_tags:
		tag_block = {}
		tag_block['key'] = tag.key
		tag_block['value'] = tag.value
		tags.append(tag_block)
	'''
	



@app.route('/dashboard')
def dashboard():
	# tag1 = Tag.query.filter_by(key=tag1).first()
	# tag2 = Tag.query.filter_by(key=tag2).first()
	labels.append('TEST')
	values.append(100)
	return render_template('dashboard.html', title='Veriler', max=17000, labels=labels, values=values)	



@app.route('/test', methods=['GET','POST'])
def test():
	 if request.method == "POST":
	 	data = request.json["data"]
	 	print(data)
	 	return Response("hey")
	 return render_template('test.html')


@app.route('/ajaxtest', methods=['GET','POST'])
def ajaxtest():
	return render_template('ajaxhtml.html')