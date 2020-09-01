import sqlite3
from flask import Blueprint, render_template, request, redirect, session
from ..db import get_db

# define our blueprint
bp = Blueprint('task_list', __name__)


@bp.route('/mylists', methods=['GET'])
def mylists():
    if 'uid' in session:
        is_logged_in = True
    else:
        is_logged_in = False

    # get the db connection
    db = get_db()

    # insert user into db
    try:
        # execute the SQL query
        mylists = db.execute(
            "SELECT * FROM TaskList WHERE user_id=?;", (str(session['uid']))).fetchall()
        return render_template('task-lists/task-lists.html', is_logged_in=is_logged_in, mylists=mylists)

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/add/list', methods=['GET', 'POST'])
def add_list():
    if request.method == 'GET':
        if 'uid' in session:
            is_logged_in = True
        else:
            is_logged_in = False

        return render_template('task-lists/add-task-list.html', is_logged_in=is_logged_in)
    else:
        list_name = request.form['list-name']
        list_description = request.form['list-description']
        user_id = session['uid']

        # get the db connection
        db = get_db()

        # insert user into db
        try:
            # execute the SQL query
            db.execute(
                "INSERT INTO TaskList (name, description, user_id) VALUES (?, ?, ?);", (list_name, list_description, user_id))

            # commit the changes to the DB
            db.commit()

            return redirect('/mylists')
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")
