from flask import Flask, jsonify, abort, make_response, request
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"
CONN = todos.create_connection("todos.db")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return todos.all()

@app.route("/api/v1/todos/<int:task_id>", methods=["GET"])
def get_todo(task_id):
    table = "tasks"
    todo = todos.select_where(table, task_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'tytuł' in request.json:
        abort(400)
    todo = {
        'Zadanie_id': todos.all()[-1]['id'] + 1,
        'tytuł': request.json['tytuł'],
        'opis': request.json.get('opis', ""),
        'status': False
    }
    todos.add_task(todo)
    return jsonify({'todo': todo}), 201

@app.route("/api/v1/todos/<int:task_id>", methods=['DELETE'])
def delete_todo(task_id):
    table = "tasks"
    result = todos.delete_where(table, task_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/todos/<int:task_id>", methods=["PUT"])
def update_todo(task_id):
    table = "tasks"
    todo = todos.select_where(table, task_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'tytuł' in data and not isinstance(data.get('tytuł'), str),
        'opis' in data and not isinstance(data.get('opis'), str),
        'status' in data and not isinstance(data.get('status'), bool)
    ]):
        abort(400)
    todo = {
        'tytuł': data.get('tytuł', todo['tytuł']),
        'opis': data.get('opis', todo['opis']),
        'status': data.get('status', todo['status'])
    }
    todos.update(task_id, todo)
    return jsonify({'todo': todo})

if __name__ == "__main__":
    app.run(debug=True)