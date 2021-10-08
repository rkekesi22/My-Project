from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required, current_user
from .models import User,Projects,Tasks,Datum
from . import db
from datetime import date



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


        if not project_name:
            project_name = 'Tasks'

        projects = Projects.query.all()

        for proj in projects:
            if proj.project_name == project_name and current_user.id == proj.user_id:
                found = True

        if not found:
            new_project = Projects(project_name, True, current_user.id)
            db.session.add(new_project)
            db.session.commit()
            projects = Projects.query.all()


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

    print(projects.__repr__())
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

    print("HAHO itt vagyok.")
    projects = Projects.query.all()

    for project in projects:
        if project.project_name == tab and current_user.id == project.user_id:
            project.active = True
        else:
            project.active = False

    db.session.commit()
    return redirect(url_for('views.currenttasks'))


@views.route('/close/<int:task_id>')
@login_required
def close_task(task_id):

    task = Tasks.query.get(task_id)

    if not task:
        return redirect(url_for('views.currenttasks'))

    if task.status:
        task.status = False
    else:
        task.status = True

    db.session.commit()
    return redirect(url_for('views.currenttasks'))


@views.route('/remove/<list_id>')
@login_required
def remove_all(list_id):
    Tasks.query.filter(Tasks.project_id==list_id).delete()
    db.session.commit()
    return redirect(url_for('views.currenttasks'))


@views.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Tasks.query.get(task_id)

    if not task:
        return redirect(url_for('views.currenttasks'))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('views.currenttasks'))


@views.route('/clear/<delete_id>')
@login_required
def clear_all(delete_id):
    Tasks.query.filter(Tasks.project_id==delete_id).delete()
    Projects.query.filter(Projects.project_id==delete_id).delete()
    db.session.commit()
    return redirect(url_for('views.currenttasks'))


honapok = {1: 'Január',
             2: 'Február',
             3: 'Március',
             4: 'Április',
             5: 'Május',
             6: 'Június',
             7: 'Július',
             8: 'Augusztus',
             9: 'Szeptember',
             10: 'Október',
             11: 'November',
             12: 'December'
    }

@views.route('/calendar')
@login_required
def calendar():
    # today = str(date.today()).split('-')
    # actual_year = today[0]
    # actual_month = today[1]
    # actual_month_name = str(honapok[int(actual_month)])
    #
    # datum = Datum.query.all()
    #
    # found = False
    #
    # for proj in datum:
    #     if current_user.id == proj.user_id:
    #         found = True
    #
    # if not found:
    #     new_datum = Datum(actual_year,actual_month_name,True, current_user.id)
    #     db.session.add(new_datum)
    #     db.session.commit()
    #     datum = Datum.query.all()
    #
    # for proj in datum:
    #     if current_user.id == proj.user_id:
    #         datum_id = proj.datum_id
    #         proj.active = True
    #     else:
    #         proj.active = False

    return render_template('calendar.html',user = current_user)


# @views.route('/next_month/<user>/<month>/<year>')
# @login_required
# def next_month(user,month,year):
#     print('Beléptem')
#     actual_month = 0
#     actual_year = int(year)
#     for i in honapok:
#         if honapok[i] == month:
#             actual_month = i
#
#     actual_month = actual_month + 1
#
#     if actual_month == 13:
#         actual_month = 1
#         actual_year = actual_year + 1
#
#     actual_month_name = str(honapok[actual_month])
#     print(actual_month_name)
#
#     update = Datum.query.filter(Datum.user_id==user).first()
#     print(update.ev)
#     print(update.honap)
#     update.ev = actual_year
#     update.honap = actual_month_name
#     db.session.commit()
#
#     return redirect(url_for('views.calendar'))
#
#
# @views.route('/last_month/<user>/<month>/<year>')
# @login_required
# def last_month(user,month,year):
#     print('Beléptem')
#     actual_month = 0
#     actual_year = int(year)
#     for i in honapok:
#         if honapok[i] == month:
#             actual_month = i
#
#     actual_month = actual_month - 1
#
#     if actual_month == 0:
#         actual_month = 12
#         actual_year = actual_year - 1
#
#     actual_month_name = str(honapok[actual_month])
#     print(actual_month_name)
#
#     update = Datum.query.filter(Datum.user_id==user).first()
#     print(update.ev)
#     print(update.honap)
#     update.ev = actual_year
#     update.honap = actual_month_name
#     db.session.commit()
#
#     return redirect(url_for('views.calendar'))
#
#
#
