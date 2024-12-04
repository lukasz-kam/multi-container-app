from .models import Todo

class TodoService:

    @staticmethod
    def get_all():
        todos = Todo.get_all()
        return [{'id': str(todo['_id']), 'title': todo['title'], 'description': todo.get('description', ''),
                 'completed': todo.get('completed', False)} for todo in todos]

    @staticmethod
    def get_by_id(todo_id):
        todo = Todo.get_by_id(todo_id)
        if todo:
            return {'id': str(todo['_id']), 'title': todo['title'], 'description': todo.get('description', ''),
                    'completed': todo.get('completed', False)}
        return None

    @staticmethod
    def create(data):
        todo = {
            'title': data['title'],
            'description': data.get('description'),
            'completed': data.get('completed', False)
        }
        return Todo.create(todo)

    @staticmethod
    def update(todo_id, data):
        todo = Todo.update(todo_id, data)

        if todo:
            return {'id': str(todo['_id']), 'title': todo['title'], 'description': todo.get('description', ''),
                    'completed': todo.get('completed', False)}
        return None

    @staticmethod
    def delete(todo_id):
        return Todo.delete(todo_id)
