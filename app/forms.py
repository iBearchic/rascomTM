from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from manage import User, Employee, Task
import os

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    secret_word = PasswordField('Ключ доступа', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            return False
        return True
    
    def validate_key(self, secret_word):
        if secret_word.data == "rascomTeam":
            return True
        return False

class TaskForm(FlaskForm):
    taskname = StringField('Название задачи', validators=[DataRequired()])
    expected_time = IntegerField('Плановое время', validators=[DataRequired(), NumberRange(min=0)])
    task_hardness = IntegerField('Степень сложности', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Создать')

class EmployeeForm(FlaskForm):
    name = StringField('Имя сотрудника', validators=[DataRequired()])
    time_available = IntegerField('Доступное время', validators=[DataRequired(), NumberRange(min=0)])
    level = IntegerField('Степень компетенции', validators=[DataRequired(), NumberRange(min=1, max=5)])
    salary = IntegerField('Зарплата', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Добавить')

class UserTaskForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    task_id = IntegerField('Task ID', validators=[DataRequired()])
    time_assigned = IntegerField('Time Assigned', validators=[DataRequired()])
    submit = SubmitField('Assign Task')
# class AssignTaskForm(FlaskForm):
#     time_assigned = IntegerField('Time Assigned', validators=[DataRequired()])
#     submit = SubmitField('Assign')
