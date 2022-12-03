from flask import Flask, redirect, render_template

from weather import weather_by_city
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from data.db_session import query_by_citi, create_session, query_what_citi, query_by_all, query_citi
from data.users import User

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # return redirect('/index')
        # '''
        db_sess = create_session()
        user = db_sess.query(User).filter(User.name == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            global what_citi
            what_citi = user.citi
            if user.name == 'SuperAdmin':
                return redirect("/super_admin")
            return redirect("/index")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    # '''
    return render_template('login.html', title='Get access', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def login_():
    return redirect('/login')


@app.route('/super_admin')
def super_admin():
    page_title = 'Super Administrator'
    q = query_by_all()
    citi_list = query_citi()
    return render_template('super_admin.html', query=q[0], counts=q[1], citi_list=citi_list, page_title=page_title)


@app.route('/index')
def index():
    page_title = 'Kraken control'
    citi_str = str(query_what_citi(what_citi))
    weather = weather_by_city(citi_str)  # по_умолч.='Moscow,Russia', можно добавить другой.
    if weather:
        weather_txt = "{}: {}, {}. Feel's like {}".format(citi_str.replace(',', ', '), *weather)
    else:
        weather_txt = 'The weather server is temporarily unavailable'  # Сервер погоды временно недоступен

    q = query_by_citi(what_citi)
    return render_template('index.html', query=q[0], counts=q[1], citi_str=citi_str, page_title=page_title, weather_text=weather_txt)


def main():
    app.run(port=8080, host='127.0.0.1', use_reloader=False, debug=True)


# if __name__ == '__main__':
#     main()
