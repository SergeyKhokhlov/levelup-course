# -*-coding: utf-8 -*-
import subprocess
import json


def task():
    with open("static/txt/id.txt") as file:
        my_id = file.readline()
    proc = subprocess.Popen(["python static/files/" + my_id + "/2/3.py"], stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE, shell=True)
    proc.stdin.write(b'\xd0\x98\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd1\x83\xd1\x8e '
                     b'\xd0\xbd\xd0\xb0\xd1\x83\xd1\x88\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb8 \xd0\xba'
                     b'\xd0\xb0\xd0\xb6\xd0\xb4\xd1\x8b\xd0\xb9 \xd0\xb4\xd0\xb5\xd0\xbd\xd1\x8c.\n')
    (out, err) = proc.communicate()
    out = out.decode("utf-8")
    print(out)
    put = "Попалось\n"
    if str(out) == put:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["2"]["3"] = 2
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    else:
        with open("static/json/tasks.json", encoding='utf-8') as file:
            js_file = json.loads(file.readline())
        with open("static/json/tasks.json", "w", encoding='utf-8') as file:
            js_file[my_id]["2"]["3"] = 1
            popular_json = json.dumps(js_file)
            file.write(popular_json)
    return 0


if __name__ == '__main__':
    task()
