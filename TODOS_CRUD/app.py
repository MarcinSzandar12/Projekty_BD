from flask import Flask, jsonify, abort, make_response, request
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    todosall = todos.all()
    return jsonify(todosall)

@app.route("/api/v1/todos/<int:task_id>", methods=["GET"])
def get_todo(task_id):
    table = "tasks"
    todo = todos.select_where(table, task_id=task_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = (
        request.json['title'],
        request.json.get('description', ""),
        False
    )
    todos.add_task(todo)
    return jsonify({'todo': todo}), 201

@app.route("/api/v1/todos/<int:task_id>", methods=['DELETE'])
def delete_todo(task_id):
    table = "tasks"
    result = todos.delete_where(table, task_id=task_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/todos/<int:task_id>", methods=["PUT"])
def update_todo(task_id):
    table = "tasks"
    todo = todos.select_where(table, task_id=task_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'status' in data and not isinstance(data.get('status'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('tytuł', todo['title']),
        'description': data.get('opis', todo['description']),
        'status': data.get('status', todo['status'])
    }
    todos.update(table, task_id, todo)
    return jsonify({'todo': todo})

if __name__ == "__main__":
    app.run(debug=True)