from flask import Flask, redirect, render_template, url_for

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


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    file = url_for('static', filename='img/photo.jpg')
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align="center">Загрузка фотографии</h1>
                            <h3 align="center">для участия в миссии</h3>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                   <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <img src="{file}" alt="Фото">
                                    <br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        with open(f'static/img/{f.filename}', 'wb') as file:
            file.write(f.read())
        file = url_for('static', filename=f'img/{f.filename}')
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <h1 align="center">Загрузка фотографии</h1>
                            <h3 align="center">для участия в миссии</h3>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                   <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <img src="{file}" alt="Фото">
                                    <br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''


def main():
    app.run(port=8080, host='127.0.0.1', use_reloader=False, debug=True)


# if __name__ == '__main__':
#     main()
