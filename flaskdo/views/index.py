from flask import Blueprint, render_template, request, redirect, session

# define our blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    if 'uid' in session:
        is_logged_in = True
    else:
        is_logged_in = False
    return render_template('index.html', is_logged_in=is_logged_in)
