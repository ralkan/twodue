from flask import Blueprint, redirect, url_for, request, g, current_app

bp = Blueprint('todos', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return "Todos!"
