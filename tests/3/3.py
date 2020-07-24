# -*-coding: utf-8 -*-
import subprocess
import json


def task():
    with open("static/txt/id.txt") as file:
        my_id = file.readline()
    proc = subprocess.Popen(["python static/files/" + my_id + "/3/3.py"], stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE, shell=True)
    proc.stdin.write(b'500\n1500')
    (out, err) = proc.communicate()
    out = out.decode("utf-8")
    put = "Компания заработала больше на 1000 рублей, чем потратила.\n"
    if str(out) == put:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 2
            popular_json = json.dumps(js_file)
            file.write(popular_json)
        task_2(my_id)
    else:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 1
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    return 0


def task_2(my_id):
    proc = subprocess.Popen(["python static/files/" + my_id + "/3/3.py"], stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE, shell=True)
    proc.stdin.write(b'15\n10')
    (out, err) = proc.communicate()
    out = out.decode("utf-8")
    put = "Компания заработала меньше на 5 рублей, чем потратила.\n"
    if str(out) == put:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 2
            popular_json = json.dumps(js_file)
            file.write(popular_json)
        task_3(my_id)
    else:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 1
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    return 0


def task_3(my_id):
    proc = subprocess.Popen(["python static/files/" + my_id + "/3/3.py"], stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE, shell=True)
    proc.stdin.write(b'485\n485')
    (out, err) = proc.communicate()
    out = out.decode("utf-8")
    put = "В этом месяце мы потратили и заработали 485 рублей.\n"
    if str(out) == put:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 2
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    else:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["3"]["3"] = 1
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    return 0


if __name__ == '__main__':
    task()
