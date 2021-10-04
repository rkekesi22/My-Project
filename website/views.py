from flask import Blueprint,render_template,request
from flask_login import login_required, current_user

views = Blueprint('views',__name__,url_prefix='/')

@views.route('/')
@login_required
def home():
    return render_template('home.html', user = current_user)


@views.route('/newtask', methods=['GET', 'POST'])
def newtask():
    if request.method == 'POST':
        project_name = request.form.get('projectName')
        task_name = request.form.get('taskName')
        status = request.form.get('status')
        task_time = request.form.get('taskTime')
        description = request.form.get('description')

    print(request.form.to_dict())

    return render_template('newtask.html', user = current_user)


@views.route('/currenttasks')
def currenttasks():
    return render_template('currenttasks.html', user = current_user)