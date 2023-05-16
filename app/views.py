from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from manage import db, User, Employee, Task
from forms import TaskForm, AssignTaskForm

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@main_blueprint.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()

    if form.validate_on_submit():
        new_task = Task(taskname=form.taskname.data, expected_time=form.expected_time.data, 
                        task_hardness=form.task_hardness.data, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully.')
        return redirect(url_for('main.home'))

    return render_template('create_task.html', form=form)

@main_blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('main.home'))

    return render_template('edit_task.html', form=form)

@main_blueprint.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('main.home'))

@main_blueprint.route('/assign_task/<int:task_id>/<int:employee_id>', methods=['POST'])
@login_required
def assign_task(task_id, employee_id):
    task = Task.query.get(task_id)
    employee = Employee.query.get(employee_id)
    form = AssignTaskForm()

    if form.validate_on_submit():
        time_assigned = form.time_assigned.data

        if employee.time_available < time_assigned:
            flash('The assigned time exceeds the employee\'s available time.')
            return redirect(url_for('main.home'))

        task.employee_id = employee_id
        task.time_assigned = time_assigned
        employee.time_available -= time_assigned
        db.session.commit()
        flash('Task assigned successfully.')
        return redirect(url_for('main.home'))

    return render_template('assign_task.html', form=form, task=task, employee=employee)

