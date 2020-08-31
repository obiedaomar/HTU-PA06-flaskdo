import sqlite3
from flask import Blueprint, render_template, request, redirect
from ..models.user import User
from ..db import get_db

# define our blueprint
bp = Blueprint('login', __name__)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # when the user requests the page over the HTTP GET
    if request.method == 'GET':
        return render_template('login/signup.html')

    # when the user submits the form over the HTTP POST
    else:
        # read values from form
        email = request.form['email']
        password = request.form['password']

        print(f"Storing {email} and {password}.")

        # get the db connection
        db = get_db()

        # insert user into db
        try:
            # execute the SQL query
            db.execute(
                "INSERT INTO User (email, password) VALUES (?, ?);", (email, password))

            # commit the changes to the DB
            db.commit()
            return redirect('/login')
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")
