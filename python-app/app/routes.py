from flask import Blueprint, request, jsonify
from .services import TodoService

api = Blueprint('api', __name__)

def init_routes(app):
    app.register_blueprint(api, url_prefix='/')

@api.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoService.get_all()
    return jsonify(todos)

@api.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = TodoService.get_by_id(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo)

@api.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    result = TodoService.create(data)
    todo_id = str(result.inserted_id)
    return jsonify({'id': todo_id}), 201

@api.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    result = TodoService.update(todo_id, data)

    if not result:
        return jsonify({'error': 'Todo not found'}), 404
    return result

@api.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    result = TodoService.delete(todo_id)

    if not result.deleted_count:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted'})
