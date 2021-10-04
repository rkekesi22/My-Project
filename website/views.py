from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required, current_user
from .models import Projects,Tasks
from . import db

views = Blueprint('views',__name__,url_prefix='/')

@views.route('/')
@login_required
def home():
    return render_template('home.html', user = current_user)


@views.route('/newtask', methods=['GET', 'POST'])
def new_task():
    return render_template('newtask.html', user = current_user)


@views.route('/currenttasks')
def currenttasks():
    pass