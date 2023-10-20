from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class BalanceForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    deposit = SubmitField('Deposit')
    withdraw = SubmitField('Withdraw')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("login called")
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:

            # new code
            #user_from_Users = user
            ##user = Charities.get_by_auth(form.email.data, form.password.data)
            #if user is None:
               # flash('Invalid email or password')
               # return redirect(url_for('users.login'))
                
            # end of new code
            flash('Invalid email or password') # I COMMENTED THIS OUT 
            return redirect(url_for('users.login')) # I COMMENTED THIS OUT
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

# @bp.route('/account', methods=['GET', 'POST'])
# def account():
#     form = BalanceForm()
#     if current_user.is_authenticated: 
#         return render_template('account.html', form=form)
    
@bp.route('/account', methods=['GET', 'POST'])    #DEPOSIT METHOD
def updateBalance():
    id = current_user.id
    form =BalanceForm()
    if form.validate_on_submit:
        amount = form.amount.data
        if amount: 
            if form.deposit.data:
                new_balance = User.get_balance(id) + amount
            elif form.withdraw.data:
                new_balance = User.get_balance(id) - amount
            User.update_balance(id, new_balance)  
            return redirect(url_for('users.updateBalance'))  #refreshes page 
    else:
        print("no balance entered")
    return render_template('account.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
