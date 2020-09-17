import sqlite3
from flask import Flask,Blueprint, render_template, request, redirect, session, url_for
from ..models.user import User
from ..db import get_db
from werkzeug.utils import secure_filename

# define our blueprint
bp = Blueprint('profile', __name__)
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@bp.route('/profile')
def view_profile():
    # get db connection
    db = get_db()
    tasklist = db.execute(
            "SELECT * FROM TaskList WHERE user_id=?;",(session['uid'],))

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            # redirect to index
            return render_template('profile/profile.html', user=user,tasklists=tasklist)
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/edit/profile', methods=['GET', 'POST'])
def edit_profile():
    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            if request.method == 'GET':
                # redirect to index
                return render_template('profile/edit-profile.html', user=user)
            else:
                email = request.form['email']
                first_name = request.form['firstname']
                last_name = request.form['lastname']
                birthdate = request.form['birthdate']
                avatarURL = request.files['avatarURL']
                avatarURL.save(secure_filename(avatarURL.filename))
                address = request.form['address']

                db.execute(
                    "UPDATE User SET email=?, firstname=?, lastname=?, birthdate=?, avatarURL=?, address=? WHERE id=?;", (email, first_name, last_name, birthdate, avatarURL, address, session['uid'],)).fetchone()

                db.commit()
                return redirect(url_for('profile.view_profile'))
                # session['firstname']=firstname
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/delete/profile')
def delete_profile():

    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        db.execute("DELETE FROM User WHERE id=?;", (session['uid'],))
        db.commit()

        return redirect(url_for("login.logout"))

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/profile/changepassword',methods=['GET', 'POST'])
def change_password():
    if request.method=="GET":
        return render_template("profile/change_password.html")
    else:
        change_password=request.form['change_password']

        # get db
        db=get_db()
        try:
            db.execute("UPDATE USER SET password=? WHERE id=?;",(change_password,session['uid'],)).fetchone()
            db.commit()
            print("password is ",change_password)
            return redirect("/login")

        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return redirect("/404")