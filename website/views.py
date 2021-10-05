from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required, current_user
from .models import User,Projects,Tasks
from . import db

views = Blueprint('views',__name__,url_prefix='/')

@views.route('/')
@login_required
def home():
    return render_template('home.html', user = current_user)


@views.route('/newtask', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':

        found = False

        data = request.form.to_dict()
        project_name = request.form.get('projectName')

        print("project_name: " + project_name)
        print("bool(project_name): " + str(bool(project_name)))

        if not project_name:
            project_name = 'Tasks'

        print("project_name: " + project_name)

        projects = Projects.query.all()
        print("projects: " + str(projects))
        for proj in projects:
            print(proj.project_name + "-----" + project_name)
            if proj.project_name == project_name:
                found = True

        if not found:
            new_project = Projects(project_name, True, current_user.id)
            db.session.add(new_project)
            db.session.commit()
            projects = Projects.query.all()

        print("projects: " + str(projects))

        for proj in projects:
            print(proj.project_name + "-----" + project_name)
            if proj.project_name == project_name:
                project_id = proj.project_id
                proj.active = True
            else:
                proj.active = False

        status = bool(int(request.form['status']))
        print(request.form['status'])

        new_task = Tasks(project_id,data.get('taskName'),status,data.get('taskTime'),data.get('description'))
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('views.currenttasks'))

    return render_template('newtask.html', user=current_user)


@views.route('/currenttasks')
def currenttasks():
    return render_template('currenttasks.html', user=current_user)