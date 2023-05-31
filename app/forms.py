from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
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
    taskname = StringField('Task Name', validators=[DataRequired()])
    expected_time = IntegerField('Expected Time', validators=[DataRequired()])
    task_hardness = IntegerField('Task Hardness', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserTaskForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    task_id = IntegerField('Task ID', validators=[DataRequired()])
    time_assigned = IntegerField('Task Assigned', validators=[DataRequired()])
    submit = SubmitField('Assign Task')
# class AssignTaskForm(FlaskForm):
#     time_assigned = IntegerField('Time Assigned', validators=[DataRequired()])
#     submit = SubmitField('Assign')
