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
            if proj.project_name == project_name and current_user.id == proj.user_id:
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

        new_task = Tasks(project_id,data.get('taskName'),status,data.get('taskTime'),data.get('description'),current_user.id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('views.currenttasks'))

    return render_template('newtask.html', user=current_user)


@views.route('/currenttasks')
@login_required
def currenttasks():
    active = None
    projects = Projects.query.all()
    tasks = Tasks.query.all()

    print("projects:")
    print(projects.__repr__())
    print("tasks: ")
    print(tasks.__repr__())


    if len(projects) == 1:
        projects[0].active = True
        active = projects[0].project_id
        db.session.commit()

    if projects:
        for project in projects:
            print(project)
            print(project.project_id)
            print(project.active)
            if project.active:
                active = project.project_id

            print(bool(active))
        if not active:
            print('Beléptem')
            projects[0].active = True
            active = projects[0].project_id
    else:
        projects = None

    if projects:
        return render_template('currenttasks.html', tasks=tasks, projects=projects, active=active, user=current_user)
    else:
        return render_template('currenttasks.html', tasks=tasks, active=active, user=current_user)


@views.route('/project/<tab>')
@login_required
def tab_nav(tab):
    """Switches between active tabs"""
    projects = Projects.query.all()

    for project in projects:
        if project.project_name == tab and current_user.id == project.user_id:
            project.active = True
        else:
            project.active = False

    db.session.commit()
    return redirect(url_for('views.currenttasks'))