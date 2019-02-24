import os

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, logout_user, login_user, current_user

from models.user import User
from models.question import Question
from database import init_db, db
from forms.login_form import LoginForm
from forms.question_form import QuestionForm
from forms.answer_form import AnswerForm
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
    user2.questions = [Question(detail='aaa?', answer='bbb!')]
    db.session.commit()


add_user()

# flask-loginを設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/registration', methods=['POST'])
def registration():
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        users = User.query.filter_by(name=login_form.name.data).all()
        if len(users) > 0 and compare_password(login_form.password.data, users[0].password_hash, users[0].salt):
            login_user(users[0])
            return redirect(url_for('dashboard'))
    else:
        print('Not Validated')
    return render_template('login.html', form=login_form)


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    questions = Question.query.all()
    user_questions = []
    if current_user.is_authenticated:
        user_questions = Question.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', questions=questions, user_questions=user_questions)


@app.route('/user/<user_name>', methods=['GET', 'POST'])
def show_user_profile(user_name):
    question_form = QuestionForm()
    users = User.query.filter_by(name=user_name).all()
    if len(users) == 0:
        user = None
    else:
        user = users[0]
        if question_form.validate_on_submit():
            print('question : {}'.format(question_form.question.data))
            question = Question(detail=question_form.question.data, user_id=user.id)
            db.session.add(question)
            db.session.commit()
    return render_template('user_profile.html', user=user, form=question_form)


@app.route('/answer', methods=['POST'])
def answer():
    answer_form = AnswerForm()
    # 存在しない質問に回答する事、本人以外が回答する事は考慮しない
    question = Question.query.filter_by(id=answer_form.question_id.data)[0]
    if answer_form.validate_on_submit():
        question.answer = answer_form.answer.data
        db.session.add(question)
        db.session.commit()
    user = question.user
    return render_template('user_profile.html', user=user, form=QuestionForm())


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    for u in User.query.all():
        # TODO debug
        print('{}, {}, {}, {}'.format(u.id, u.name, u.password_hash, u.salt, u.created_at, u.updated_at))
        print(u.questions)

    app.run()
