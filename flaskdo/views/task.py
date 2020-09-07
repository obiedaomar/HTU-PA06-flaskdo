import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for
from ..db import get_db
from ..models.priority import Priority

# define our blueprint
bp = Blueprint('task', __name__)

priorities = {
    Priority.LOW.value: Priority.LOW.name,
    Priority.MEDIUM.value: Priority.MEDIUM.name,
    Priority.HIGH.value: Priority.HIGH.name
}


@bp.route('/add/task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'GET':

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


@bp.route('/update/task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    # get db connection
    db = get_db()

    # fetch task list
    try:
        # execute the SQL query
        task = db.execute(
            "SELECT * FROM Task WHERE id=?", (task_id,)).fetchone()

        # if the task was found
        if task:
            if request.method == 'GET':
                # execute the SQL query
                tasklists = db.execute(
                    "SELECT id, name FROM TaskList WHERE user_id=?;", (session['uid'],)).fetchall()
                return render_template('tasks/update-task.html', task=task, priorities=priorities, tasklists=tasklists)
            else:
                title = request.form['task-title']
                description = request.form['task-description']
                priority = request.form['prioritySelect']
                task_list_id = request.form['taskListSelect']

                # update task in DB
                tasks = db.execute('UPDATE Task SET title=?, description=?, priority=?, task_list_id=? WHERE id = ?', (
                    title, description, priority, task_list_id, task_id,))

                # write changes to DB
                db.commit()

                # render_template to 'task-list'
                return redirect(url_for('task.view_task', task_id=task_id))

        # if the tasklist was not found
        else:
            # redirect to 404
            return redirect("/404")

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/task/<int:task_id>', methods=['GET', 'POST'])
def view_task(task_id):

    # get db connection
    db = get_db()

    # fetch the task
    try:
        # execute the SQL query
        task = db.execute(
            "SELECT * FROM Task WHERE id=?", (task_id,)).fetchone()

        # if the tasklist was found
        if task:
            # render_template to 'tasks/view-task.html'
            return render_template('tasks/view-task.html', task=task)

        # if the tasklist was not found
        else:
            # redirect to 404
            return redirect("/404")

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/mytasks')
def mytasks():
    # get db connection
    db = get_db()

    # fetch all user tasks
    try:
        # execute the SQL query
        tasks = db.execute(
            'SELECT t.id, t.title, t.description, tl.id, tl.name FROM TaskList tl JOIN Task t ON tl.user_id = ? AND tl.id = t.task_list_id',
            (session['uid'],))

        return render_template('tasks/mytasks.html', tasks=tasks)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/delete/task/<int:task_id>')
def delete_task(task_id):
    # get db connection
    db = get_db()

    try:
        # delete task from DB
        db.execute("DELETE FROM Task WHERE id=?;", (task_id,))

        # write changes to the DB
        db.commit()

        # redirect to the 'view_list' view
        return redirect(url_for('task_list.mylists'))
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")
