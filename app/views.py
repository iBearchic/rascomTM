from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from manage import db, User, Employee, Task, UserTask
from forms import TaskForm, EmployeeForm
from utils.optimizer import Optimizer
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@login_required
def home():
    tasks = Task.query.all()
    employees = Employee.query.all()
    return render_template('home.html', tasks=tasks, employees=employees)

@main_blueprint.route('/create_employee', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = EmployeeForm()
    if request.method == "POST":
        employee = Employee(name=form.name.data, time_available=form.time_available.data, level=form.level.data, salary=form.salary.data)
        db.session.add(employee)
        db.session.commit()
        flash(f'Сотрудник "{form.name.data}" успешно добавлен!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_employee.html', form=form)

@main_blueprint.route('/edit_employee/<employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee is None:
        flash(f'Сотрудник с номером {employee_id} не найден', 'danger')
        return redirect(url_for('main.home'))
    
    form = EmployeeForm(obj=employee)
    if request.method == "POST":
        employee.name = form.name.data
        employee.time_available = form.time_available.data
        employee.level = form.level.data
        employee.salary = form.salary.data
        db.session.commit()
        flash(f'Сотрудник "{form.name.data}" успешно обновлен', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('edit_employee.html', form=form)

@main_blueprint.route('/delete_employee/<employee_id>', methods=['GET', 'POST'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee is None:
        flash(f'Сотрудник с номером {employee_id} не найден', 'danger')
        return redirect(url_for('main.home'))
    
    db.session.delete(employee)
    db.session.commit()
    flash(f'Сотрудник с номером {employee_id} успешно удален', 'success')
    return redirect(url_for('main.home'))

@main_blueprint.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if request.method == "POST":
        task = Task(taskname=form.taskname.data, expected_time=form.expected_time.data, task_hardness=form.task_hardness.data)
        db.session.add(task)
        db.session.commit()
        flash(f'Задача "{form.taskname.data}" успешно создана!', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_task.html', form=form)

@main_blueprint.route('/edit_task/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        flash(f'Задача с номером {task_id} не найдена', 'danger')
        return redirect(url_for('main.home'))
    
    form = TaskForm(obj=task)
    if request.method == "POST":
        task.taskname = form.taskname.data
        task.expected_time = form.expected_time.data
        task.task_hardness = form.task_hardness.data
        db.session.commit()
        flash(f'Задача "{form.taskname.data}" успешно обновлена', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('edit_task.html', form=form)

@main_blueprint.route('/delete_task/<task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        flash(f'Задача с номером {task_id} не найдена', 'danger')
        return redirect(url_for('main.home'))
    
    db.session.delete(task)
    db.session.commit()
    flash(f'Задача с номером {task_id} успешно удалена', 'success')
    return redirect(url_for('main.home'))

@main_blueprint.route('/optimize/<mode>', methods=['GET', 'POST'])
@login_required
def optimize(mode):
    tasks = Task.query.all()
    employees = Employee.query.all()

    if mode == "time":
        op = Optimizer()
        res = op.start(tasks, employees, mode)
        flash('Оптимальный план по срокам построен ниже!', 'success')
        return render_template('home.html', tasks=tasks, employees=employees, optimum=res)
    elif mode == "cost":
        op = Optimizer()
        res = op.start(tasks, employees, mode)
        flash('Оптимальный план по бюджету построен ниже!', 'success')
        return render_template('home.html', tasks=tasks, employees=employees, optimum=res)
    else:
        flash('Что-то пошло не так', 'warning')
        return redirect(url_for('main.home'))


