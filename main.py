# -*-coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session, users, registration, login_class, edit_profile_form, forum_db, \
    ask_question, btn_save_form
import os
import pymorphy2
import json
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'courses_PRODUCT_KHOKHLOV'
login_manager = LoginManager()
login_manager.init_app(app)
bot_icon = 0


def count_users():
    sessions = db_session.create_session()
    all_users = sessions.query(users.User).filter(users.User.id).all()
    morph = pymorphy2.MorphAnalyzer()
    parse_word = morph.parse("человек")[0]
    true_word = parse_word.make_agree_with_number(int(len(all_users))).word
    line = str(len(all_users)) + " " + true_word
    return line


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


@app.route('/logout', methods=["GET", "POST"])  # Выйти из аккаунта
def logout():
    logout_user()
    return redirect('/')


@app.route("/", methods=["GET", "POST"])
def index():
    line = count_users()
    try:
        if len(current_user.email) != 0:
            return redirect("/courses")
    except Exception:
        message = ""
        form = registration.RegisterForm()
        sessions = db_session.create_session()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', form=form, message="Пароли не совпадают!",
                                       line=line)
            if sessions.query(users.User).filter(users.User.email == form.email.data).first():
                return render_template('register.html', form=form, line=line,
                                       message="Данный email уже занят")
            if len(form.name.data) > 20:
                return render_template('register.html', form=form, line=line,
                                       message="Данное имя слишком длинное!")
            user = users.User(name=form.name.data,
                              email=form.email.data,
                              password=form.password.data,
                              role="user",
                              raiting=0)
            user.set_password(form.password.data)
            sessions.add(user)
            sessions.commit()
            return redirect('/login')
        return render_template("index.html", form=form, line=line)


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = registration.RegisterForm()
    sessions = db_session.create_session()
    line = count_users()
    if form.validate_on_submit():
        form = registration.RegisterForm()
        sessions = db_session.create_session()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', form=form, message="Пароли не совпадают!",
                                       line=line)
            if sessions.query(users.User).filter(users.User.email == form.email.data).first():
                return render_template('register.html', form=form, line=line,
                                       message="Данный email уже занят")
            if len(form.name.data) > 20:
                return render_template('register.html', form=form, line=line,
                                       message="Данное имя слишком длинное!")
            user = users.User(name=form.name.data,
                              email=form.email.data,
                              password=form.password.data,
                              role="user",
                              raiting=0)
            user.set_password(form.password.data)
            sessions.add(user)
            sessions.commit()
            return redirect('/login')
        return render_template("index.html", form=form, line=line)
    return render_template('register.html', form=form, line=line)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    line = count_users()
    form = login_class.LoginForm()
    sessions = db_session.create_session()
    if form.validate_on_submit():
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        password = generate_password_hash(form.password.data)
        if user and check_password_hash(password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неверное имя пользователя или пароль',
                               form=form, line=line)
    return render_template("login.html", form=form, message=message, line=line)


@app.route("/courses", methods=["GET", "POST"])
def courses():
    line = count_users()
    args = []
    with open("static/json/tasks.json", encoding="utf-8") as file:
        data = json.loads(file.readline())
        for i in data:
            args.append(i)
    with open("static/json/base_tasks.json", encoding="utf-8") as file:
        temp = json.loads(file.readline())
        temp[str(current_user.id)] = temp.pop("0")
    with open("static/json/tasks.json", "w", encoding="utf-8") as file:
        if str(current_user.id) not in args:
            data.update(temp)
        json.dump(data, file)
    return render_template("courses.html", line=line)


@app.route("/profile/<int:id>", methods=["GET", "POST"])  # Профиль
@login_required
def user_info(id):
    line = count_users()
    sessions = db_session.create_session()
    user = sessions.query(users.User).get(id)
    if user:
        user_id_str = str(user.id)
        return render_template("profile.html", user=user, userid=user_id_str, line=line)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    line = count_users()
    form = edit_profile_form.EditProfileForm()
    message = "Если вы хотите изменить свой пароль, введите свой старый пароль"
    if request.method == "POST":
        session = db_session.create_session()
        if form.old_password.data != "" and form.new_password.data != "":
            if not current_user.check_password(form.old_password.data):
                message = "Неверный старый пароль"
                return render_template("edit_profile.html", form=form, line=line,
                                       message=message)
            elif form.new_password.data != form.new_password_again:
                message = "Новый пароль повторен неправильно"
                return render_template("edit_profile.html", form=form, line=line,
                                       message=message)
            elif form.old_password.data == form.new_password.data:
                message = "Новый пароль совпадает со старым"
                return render_template("edit_profile.html", form=form, line=line,
                                       message=message)
            else:
                current_user.set_password(form.new_password.data)
        if str(request.files["file"]) != "<FileStorage: '' ('application/octet-stream')>":
            file = request.files["file"]
            name = "static/img/avatar_img/avatar_" + \
                   str(1 + len(os.listdir("static/img/avatar_img"))) + ".jpg"
            file.save(name)
            current_user.avatar = "/" + name
        if form.name.data != "":
            if len(form.name.data) > 20:
                message = "Этот логин слишком длинный"
                return render_template("edit_profile.html", form=form, line=line,
                                       message=message)
            current_user.name = form.name.data
        session.merge(current_user)
        session.commit()
        return redirect(f'/profile/{current_user.id}')
    form.avatar.data = current_user.avatar
    form.name.data = current_user.name
    return render_template("edit_profile.html", form=form, message=message, line=line)


@app.route("/courses/<string:language>", methods=["GET", "POST"])
def page_course(language):
    line = count_users()
    with open("static/json/py_course.json", encoding="utf-8") as file:
        all_file = json.loads(file.readline())
        all_courses = []
        for i in range(1, 4):
            all_courses.append(all_file[str(i)])
        names_courses = []
        for i in range(3):
            names_courses.append(all_courses[i].keys())
        for i in range(len(names_courses)):
            names_courses[i] = str(names_courses[i]).split("'")[1]
    return render_template("page_course.html", line=line, language=language,
                           names_courses=names_courses)


@app.route("/courses/<string:language>/course/<int:num>", methods=["GET", "POST"])
def course(language, num):
    line = count_users()
    with open("static/json/py_course.json", encoding="utf-8") as file:
        all_file = json.loads(file.readline())
        all_courses = []
        all_courses.append(all_file[str(num)])
        names_courses = []
        names_courses.append(all_courses[0].keys())
        names_courses = str(names_courses[0]).split("'")[1]
        all_task = []
        all_task.append(all_courses[0][names_courses])
        names_task = []
        for i in all_task:
            names_task.append(i.keys())
        names_tasks = \
            str(names_task[0]).split('dict_keys')[-1].split('(')[-1].split(')')[0].split("[")[
                -1].split(
                "]")[0].split(',')
        for i in range(len(names_tasks)):
            names_tasks[i] = names_tasks[i].split("'")[1]
    return render_template("course.html", line=line, language=language, names_tasks=names_tasks,
                           num=num)


@app.route("/courses/<string:language>/course/<int:num>/task/<int:num_task>",
           methods=["GET", "POST"])
def task(language, num, num_task):
    line = count_users()
    form = btn_save_form.Btn()
    with open("static/txt/id.txt", "w", encoding="utf-8") as file:
        file.write(str(current_user.id))
    with open("static/json/py_course.json", encoding="utf-8") as json_file:
        all_file = json.loads(json_file.readline())
        all_courses = []
        all_courses.append(all_file[str(num)])
        names_courses = []
        names_courses.append(all_courses[0].keys())
        names_courses = str(names_courses[0]).split("'")[1]
        all_task = []
        all_task.append(all_courses[0][names_courses])
        names_task = []
        for i in all_task:
            names_task.append(i.keys())
        names_tasks = \
            str(names_task[0]).split('dict_keys')[-1].split('(')[-1].split(')')[0].split("[")[
                -1].split(
                "]")[0].split(',')
        for i in range(len(names_tasks)):
            names_tasks[i] = names_tasks[i].split("'")[1]
        condition_task = []
        for i in all_task:
            for j in range(len(names_tasks)):
                condition_task.append(i[names_tasks[j]])
        input_in_task = None
        output_in_task = None
        if "#$" in condition_task[num_task - 1] and "$#" in condition_task[num_task - 1]:
            input_in_task = condition_task[num_task - 1].split("#$")[1].split("$#")[0]
            output_in_task = condition_task[num_task - 1].split("#$")[1].split("$#")[1]
            condition_task = condition_task[num_task - 1].split("#$")[0]
        elif "#$" not in condition_task[num_task - 1] and "$#" in condition_task[num_task - 1]:
            output_in_task = condition_task[num_task - 1].split("$#")[1]
            condition_task = condition_task[num_task - 1].split("$#")[0]
        else:
            condition_task = condition_task[num_task - 1]
        if "<br>" in str(input_in_task) and "<br>" in str(output_in_task):
            input_in_task = input_in_task.split("<br>")
            output_in_task = output_in_task.split("<br>")
        elif "<br>" in str(input_in_task) and "<br>" not in str(output_in_task):
            input_in_task = input_in_task.split("<br>")
            output_in_task = [output_in_task]
        elif "<br>" in str(output_in_task) and "<br>" not in str(input_in_task):
            output_in_task = output_in_task.split("<br>")
            input_in_task = [input_in_task]
        else:
            output_in_task = [output_in_task]
            input_in_task = [input_in_task]
        score = 0
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
            if js_file[str(current_user.id)][str(num)][str(num_task)] == 2:
                score = 2
            elif js_file[str(current_user.id)][str(num)][str(num_task)] == 1:
                score = 1
        if form.validate_on_submit():
            if str(request.files["file"]) != "<FileStorage: '' ('application/octet-stream')>":
                file = request.files["file"]
                try:
                    name = "static/files/" + str(current_user.id) + "/" + str(num) + "/" + \
                           str(num_task) + ".py"
                    file.save(name)
                except Exception:
                    path = "static/files/" + str(current_user.id) + "/" + str(num)
                    os.makedirs(path)
                    name = "static/files/" + str(current_user.id) + "/" + str(num) + "/" + \
                           str(num_task) + ".py"
                    file.save(name)
                os.system("python tests/" + str(num) + "/" + str(num_task) + ".py")
                score = 0
                with open("static/json/tasks.json", encoding='utf-8') as file:
                    js_file = json.loads(file.readline())
                    if js_file[str(current_user.id)][str(num)][str(num_task)] == 2:
                        score = 2
                        session = db_session.create_session()
                        current_user.raiting += 1
                        session.merge(current_user)
                        session.commit()
                    elif js_file[str(current_user.id)][str(num)][str(num_task)] == 1:
                        score = 1
                return render_template("task.html", line=line, language=language,
                                       names_tasks=names_tasks[num_task - 1],
                                       condition_task=condition_task, num=num,
                                       input_in_task=input_in_task, score=score,
                                       output_in_task=output_in_task, form=form)
    return render_template("task.html", line=line, language=language,
                           names_tasks=names_tasks[num_task - 1],
                           condition_task=condition_task, num=num, input_in_task=input_in_task,
                           output_in_task=output_in_task, form=form, score=score)


@app.route("/courses/<string:language>/course/<int:num>/documentation", methods=["GET", "POST"])
def documentation(language, num):
    line = count_users()
    sessions = db_session.create_session()
    if str(current_user.documentation.split("_")[-2]) == str(num):
        return redirect("/courses/" + language + "/course/" + str(num))
    else:
        with open("static/txt/documentation/" + str(num) + ".txt", encoding="utf-8") as file:
            doc = file.readlines()
        doc = [x.rstrip() for x in doc]
        user = sessions.query(users.User).filter(users.User.id).first()
        user.documentation = str(current_user.documentation) + str(num) + "_"
        sessions.commit()
        return render_template("documentation.html", line=line, doc=' '.join(doc), num=num,
                               language=language)


@app.route("/courses/<string:language>/course/<int:num>/doc", methods=["GET", "POST"])
def doc_func(language, num):
    line = count_users()
    with open("static/txt/documentation/" + str(num) + ".txt", encoding="utf-8") as file:
        doc = file.readlines()
    doc = [x.rstrip() for x in doc]
    return render_template("documentation.html", line=line, doc=doc, num=num,
                           language=language)


@app.route("/forum", methods=["GET", "POST"])
def forum_func():
    line = count_users()
    sessions = db_session.create_session()
    forum_questions = sessions.query(forum_db.Forum).filter(forum_db.Forum.date).all()
    return render_template("forum.html", forum_questions=forum_questions, line=line)


@app.route("/forum/ask_question", methods=["GET", "POST"])  # Страница для задавания вопроса (форум)
def ask_a_question():
    form = ask_question.Ask_question()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        forum_ask_question = forum_db.Forum(
            title=str(form.title.data),
            question=str(form.question.data),
            theme=str(form.theme.data)
        )
        sessions.add(forum_ask_question)
        sessions.commit()
        return redirect("/forum")
    return render_template("ask_question.html", form=form)


@app.route("/forum/question/<int:num_id>", methods=["GET", "POST"])
def forum_full_question(num_id):
    sessions = db_session.create_session()
    forum_question = sessions.query(forum_db.Forum).filter(
        forum_db.Forum.id == num_id).first()
    name_users = []
    answers = []
    try:
        for i in forum_question.user_id.split("/end/new_author/"):
            if i != "None":
                name_users.append(sessions.query(users.User).filter(
                    users.User.id == i).first().name)
        for i in forum_question.answers.split("/end/new_answer/"):
            if i != "None":
                answers.append(i)
    except AttributeError:
        pass
    return render_template("forum_full_question.html", num_id=num_id,
                           title=forum_question.title, question=forum_question.question,
                           answers=answers, user_name=name_users, count=len(answers))


@app.route("/itnews")
def itnews():
    line = count_users()
    return render_template("itnews.html", line=line)


@app.route("/settings")
def settings():
    line = count_users()
    return render_template("settings.html", line=line)


@app.route("/helper")
def helper():
    line = count_users()
    return render_template("helper.html", line=line)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
