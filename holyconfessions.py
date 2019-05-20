from flask import Flask, render_template
app = Flask(__name__)


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




@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run(debug=True)