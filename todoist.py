from flask import Flask, render_template, request, jsonify
from todoist_api_python.api import TodoistAPI
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/todoist": {"origins": "https://fiftylist.vercel.app/"}})
data = None  

@app.route('/todoist', methods= {'GET', 'POST'})
def todoist():
    global data
    data = request.data.decode('utf-8')
    print("/TODOIST - ", data)
    return render_template('todoist.html')

@app.route('/export_todoist', methods=['GET', 'POST'])
def get_todoist_projects():
    try:
        global data  
        print("/EXPORT_TODOIST - ", data)
        api_key = request.form.get('api_key')
        api = TodoistAPI(api_key)
        projects = api.get_projects()
        return render_template('projects.html', projects=projects, api_key=api_key, data=data)
    except Exception as error:
        return jsonify({"error": str(error)})

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    try:
        global data 
        if data is None:
            return jsonify({"error": "No data received"})
        project_id = request.form.get('project_id')
        api_key = request.form.get('api_key')
        api = TodoistAPI(api_key)
        print("Adding task with description:", data)
        task = api.add_task(content='FiftyList - Your top 50 Spotify Jams', description=data, project_id=project_id)
        print("Task Response:", task)
        return render_template('task_result.html', task=task)
    except Exception as error:
        return jsonify({"error": str(error)})


if __name__ == '__main__':
    app.run(debug=False)
