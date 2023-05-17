from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False, default="default")

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    time_available = db.Column(db.Float, nullable=False, default=0.0)
    level = db.Column(db.Integer, nullable=False, default=1)
    salary = db.Column(db.Float, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(64))
    expected_time = db.Column(db.Integer)
    task_hardness = db.Column(db.Integer)

class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    employee = db.relationship('Employee', backref='usertasks')
    task = db.relationship('Task', backref='usertasks')
    time_assigned = db.Column(db.Float, nullable=False, default=0.0)
