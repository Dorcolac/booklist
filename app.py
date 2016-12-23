from flask import Flask, render_template, request, session, abort, g, url_for, redirect, flash
import sqlite3, datetime, time
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def home():
	return render_template('index.html')

@app.route("/post")
def post():
	year = time.strftime("%Y")
	print year
	return render_template('post.html', year = year)

@app.route('/addbook',methods = ['POST', 'GET'])
def addbook():
	msg = ""
	if request.method == 'POST': 
		try:
			title = request.form['title']
			author = request.form['author']
			publisher = request.form['publisher']
			year = request.form['year']

			with sqlite3.connect("books.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO books (title,author,publisher,year) VALUES (?,?,?,?)",(title,author,publisher,year) )
				con.commit()
				msg = "Successfully added!"

		except Exception as e:
			print e.message
			con.rollback()
			msg = "Error while adding."

	return render_template("fin.html", msg = msg)

@app.route('/book-list', methods = ['GET'])
def books():	
	con = sqlite3.connect("books.db")
	con.row_factory = sqlite3.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM books")

	rows = cur.fetchall()
	return render_template("books.html", rows = rows)

@app.route('/deletebook/<bookid>')
def deletebook(bookid):
		con = sqlite3.connect("books.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("DELETE FROM books WHERE bookid='" + bookid + "'")
		con.commit()
		return redirect('/book-list')

if __name__ == '__main__':
	app.run(debug = True)