from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from .models import Projects,Tasks
from . import db

from .date import *
import datetime

views = Blueprint('views',__name__,url_prefix='/')

def write_date_text():
    with open('date.txt', mode='w') as f:
        year = datetime.date.today().year
        month = datetime.date.today().month
        f.write(str(year) + "/" + str(month))
        f.close()


@views.route('/', methods = ["GET","POST"])
@login_required
def home():
    write_date_text()
    year = today_date.year
    month = today_date.month
    day = today_date.day
    day_name = days[today_date.today().weekday()]
    date_task = datetime.date(year=year, month=month, day=day)
    this_month = one_month(month, year)



    if request.method == 'GET':
        return render_template('home.html', user = current_user, day_name = day_name, today_date = today_date,
                               month_name=this_month[3],short_day_names=short_day_names,months=this_month[0],week=this_month[4])




@views.route('/newtask', methods=['GET', 'POST'])
@login_required
def new_task():
    write_date_text()
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
    write_date_text()
    active = None
    projects = Projects.query.all()
    tasks = Tasks.query.all()

    # print(projects.__repr__())
    # print(tasks.__repr__())


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


@views.route('/calendar')
@login_required
def calendar():
    year = 0
    month = 0
    with open("date.txt", "r") as f:
        d = f.read().split("/")
        year = d[0]
        month = d[1]
        f.close

    print(year)
    print(month)
    week = short_day_names
    this_month = one_month(month, year)
    if this_month is False:
        abort(404)
    months_name = months[1:]
    href = f'/{year}/{month}/'
    return render_template('calendar.html', user = current_user, months_name=months_name, months=this_month[0], le=this_month[1],
                                   year=this_month[2], month_name=this_month[3], week=week, href=href )


@views.route("/last_month/<year>/<month_name>")
@login_required
def last_month(year,month_name):
    month = months.index(month_name)

    year2 = int(year)

    if month == 1:
        month = 12
        year2 = year2 - 1
        with open("date.txt",'w') as f:
            f.write(str(year2) + "/" + str(month))
            f.close()
        return redirect(url_for('views.calendar'))
    else:
        month =  month - 1
        with open("date.txt",'w') as f:
            f.write(str(year) + "/" + str(month))
            f.close()
        return redirect(url_for('views.calendar'))


@views.route("/next_month/<year>/<month_name>")
@login_required
def next_month(year,month_name):
    month = months.index(month_name)

    year2 = int(year)

    if month == 12:
        month = 1
        year2 = year2 + 1
        with open("date.txt",'w') as f:
            f.write(str(year2) + "/" + str(month))
            f.close()
        return redirect(url_for('views.calendar'))
    else:
        month =  month + 1
        with open("date.txt",'w') as f:
            f.write(str(year) + "/" + str(month))
            f.close()
        return redirect(url_for('views.calendar'))


@views.route("/<int:year>")
@login_required
def one_year_view(year):
    months_name_list = months
    week_day_name = short_day_names
    this_year = one_year(year)
    href = f'/{year}/'
    return render_template('year.html', user=current_user, href=href, year_calendar=this_year[0], len_calendar_months=this_year[1],
                           year=this_year[2], months_name_list=months_name_list, week_day_name=week_day_name)


@views.route("/last_year/<year>")
@login_required
def last_year(year):
    year2 = int(year) -1
    return redirect(f"/{year2}")


@views.route("/next_year/<year>")
@login_required
def next_year(year):
    year2 = int(year) +1
    return redirect(f"/{year2}")


@views.route("/<href>/<int:number>")
@login_required
def control(href,number):
    year2 = int(href)
    with open("date.txt", 'w') as f:
        f.write(str(year2) + "/" + str(number))
        f.close()
    return redirect(url_for('views.calendar'))
















