from flask import Blueprint, render_template, request, redirect, session

# define our blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
