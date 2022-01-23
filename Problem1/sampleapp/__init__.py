from cmath import e
import json
from re import template
from tkinter import E


def main(env, request_handler, method):
    """Simple to do app

    Args:
        env (Environment): renders environment for our template
        request_handler(Request_handler): instance of request handler
        method(str): GET or POST
    """
    if method == "POST":
        content_length = int(request_handler.headers['Content-Length'])  # <--- Gets the size of data
        post_data = request_handler.rfile.read(content_length)  # <--- Gets the data itself\
        post_data = post_data.decode()
        # convert url data into dictionary 
        items = []
        for x in post_data.split('&'):
            items.append(x.split('='))
        post_data = dict(items)
        # check for the data in new.txt file. If there is data update the tasklist
        # if not create a new file and use it to store the tasks
        try:
            with open('new.txt', 'r+') as f:
                data = f.read()
                if data:
                    data = json.loads(data)
                    data['tasks'] += [post_data['taskname']] 
                else:
                    data = { 'tasks': [post_data['taskname']] }
        except FileNotFoundError:
            data = { 'tasks': [post_data['taskname']] }
            
        with open('new.txt', 'w') as f:
            f.write(json.dumps(data))
            
            template = env.get_template('task.html')
            return template.render(**data)

    template = env.get_template('new.html')
    return template.render()
   