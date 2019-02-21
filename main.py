import os

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, logout_user, login_user, login_required, current_user

from models.user import User
from models.question import Question
from database import init_db, db
from util.hash_util import create_salt, calculate_password_hash, compare_password

app = Flask(__name__)
# セッションを使うためにシークレットキーが必要です
app.secret_key = 'secret key'
db_name = 'test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
if os.path.exists(db_name):
    os.remove(db_name)

init_db(app)
app.app_context().push()


def add_user():

    def create_user(name, password):
        salt = create_salt()
        password_hash = calculate_password_hash(password, salt)
        return User(name=name, password_hash=password_hash, salt=salt)

    db.create_all()

    user1 = create_user('a', "aa")
    user2 = create_user('b', "bb")
    user3 = create_user('c', "cc")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    user1.questions = [Question(detail='x?', answer='yy!'), Question(detail='z?')]
    db.session.commit()


add_user()

# flask-loginを設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    print('load_user  user_id : {}'.format(user_id))
    return User.query.get(user_id)


@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/registration', methods=['POST'])
def registration():
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    from forms.login_form import LoginForm
    form = LoginForm()
    print(request.form)
    if form.validate_on_submit():
        print('Validated')
        # print('{}, {}'.format(form.name.data, form.password.data))
        users = User.query.filter_by(name=form.name.data).all()
        if len(users) > 0 and compare_password(form.password.data, users[0].password_hash, users[0].salt):
            login_user(users[0])
            return redirect(url_for('dashboard'))
    else:
        print('Not Validated')
    return render_template('login.html', form=form)


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    questions = Question.query.all()
    user_questions = []
    print(current_user)
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        print(dir(current_user))
        print(current_user.id)
        print(current_user.get_id())
        print(current_user.name)
        print(current_user.password_hash)
        print([u.user_id for u in Question.query.all()])
        print(Question.query.filter_by(user_id=current_user.id).all())
        user_questions = Question.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', questions=questions, user_questions=user_questions)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    for u in User.query.all():
        print('{}, {}, {}, {}'.format(u.id, u.name, u.password_hash, u.salt, u.created_at, u.updated_at))
        print(u.questions)

    app.run()
