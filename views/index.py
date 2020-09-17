from flask import Blueprint, render_template, request, redirect, session
from ..db import get_db
from datetime import datetime
import time;  # This is required to include time module.

# define our blueprint
bp = Blueprint('index', __name__)
@bp.route('/', methods=['GET'])
def index():
    if 'uid' in session:
        user =session['uid']
        # get db
        db=get_db()
        users=db.execute("SELECT * FROM User WHERE id=?;",(user,))
        tasklist=db.execute("SELECT * FROM TaskList WHERE user_id=?;",(user,))
         # execute the SQL query
        tasks = db.execute(
                'SELECT t.id, t.title, t.description, tl.id, tl.name FROM TaskList tl JOIN Task t ON tl.user_id = ? AND tl.id = t.task_list_id',
                (session['uid'],))
        update_date=datetime.now()
        user_open =time.asctime( time.localtime(time.time()) )
        
        return render_template('index.html',user=user,users=users,tasklists=tasklist,tasks=tasks,update_date=update_date
        ,user_open=user_open
        )
    else:
        return render_template('index.html')