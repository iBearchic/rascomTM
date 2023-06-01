from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from manage import db, User, Employee, Task, UserTask
from forms import TaskForm, UserTaskForm

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@login_required
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@main_blueprint.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if request.method == "POST":
        task = Task(taskname=form.taskname.data, expected_time=form.expected_time.data, task_hardness=form.task_hardness.data)
        db.session.add(task)
        db.session.commit()
        flash(f'Задача с номером {id} успешно создана!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_task.html', form=form)

@main_blueprint.route('/edit_task/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get(id)
    if task is None:
        flash(f'Задача с номером {id} не найдена', 'danger')
        return redirect(url_for('main.home'))
    
    form = TaskForm(obj=task)
    if request.method == "POST":
        task.taskname = form.taskname.data
        task.expected_time = form.expected_time.data
        task.task_hardness = form.task_hardness.data
        db.session.commit()
        flash(f'Задача с номером {id} успешно обновлена', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('edit_task.html', form=form)

@main_blueprint.route('/delete_task/<task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        flash(f'Задача с номером {id} не найдена', 'danger')
        return redirect(url_for('main.home'))
    
    db.session.delete(task)
    db.session.commit()
    flash(f'Задача с номером {id} успешно удалена', 'success')
    return redirect(url_for('main.home'))

# @main_blueprint.route('/assign_task', methods=['GET', 'POST'])
# @login_required
# def assign_task():
#     form = UserTaskForm()
#     if form.validate_on_submit():
#         usertask = UserTask(employee_id=form.employee_id.data, task_id=form.task_id.data, time_assigned=form.time_assigned.data)
#         db.session.add(usertask)
#         db.session.commit()
#         flash('The task has been assigned!')
#         return redirect(url_for('main.home'))
#     return render_template('assign_task.html', form=form)

