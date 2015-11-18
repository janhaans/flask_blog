from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

app = Flask(__name__)

DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard to guess'

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = "Invalid credentials, pleas try again"
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out")
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
