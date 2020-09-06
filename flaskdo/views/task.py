import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for
from ..db import get_db
from ..models.priority import Priority

# define our blueprint
bp = Blueprint('task', __name__)


@bp.route('/add/task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'GET':
        priorities = {
            Priority.LOW.value: Priority.LOW.name,
            Priority.MEDIUM.value: Priority.MEDIUM.name,
            Priority.HIGH.value: Priority.HIGH.name
        }

        # get db connection
        db = get_db()

        # fetch the user task lists
        try:
            # execute the SQL query
            task_lists = db.execute(
                "SELECT id, name FROM TaskList WHERE user_id=?;", (session['uid'],)).fetchall()

            # if the user was found
            if task_lists:
                # render_template to 'add-task'
                return render_template('tasks/add-task.html', priorities=priorities, task_lists=task_lists)

            # if no task lists were found
            else:
                # render the login page with an error message
                return redirect("/404")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")

    else:
        title = request.form['task-title']
        description = request.form['task-description']
        priority = request.form['prioritySelect']
        task_list_id = request.form['taskListSelect']

        # get the db connection
        db = get_db()

        # insert task into db
        try:
            # execute the SQL query
            db.execute(
                "INSERT INTO Task (title, description, priority, task_list_id) VALUES (?, ?, ?, ?);", (title, description, priority, task_list_id))

            # commit the changes to the DB
            db.commit()

            return redirect(url_for('task_list.view_list', tasklist_id=task_list_id))
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")
