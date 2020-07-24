# -*-coding: utf-8 -*-
import subprocess
import json


def task():
    with open("static/txt/id.txt") as file:
        my_id = file.readline()
    proc = subprocess.Popen(["python static/files/" + my_id + "/1/2.py"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode("utf-8")
    if str(out) == "Ура\nУра\nУра\n":
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["1"]["2"] = 2
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    else:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["1"]["2"] = 1
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    return 0


if __name__ == '__main__':
    task()
