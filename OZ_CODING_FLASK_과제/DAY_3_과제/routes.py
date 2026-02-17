from flask import request, jsonify, Blueprint
from . import SessionLocal, Todo


todo_bp = Blueprint('todo', __name__)

# READ: 전체 항목 조회  
@todo_bp.route('/')
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return jsonify([{'id':t.id, 'task':t.task} for t in todos]), 200

# CREATE
@todo_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    db.close()
    if not todo:
        return jsonify({'error' : '에러발생'}), 404
    return jsonify({'id' : todo.id, 'task' : todo.task}), 200
    
# READ
@todo_bp.route('/todos', methods=['POST'])
def create_todo():              
    data = request.get_json()  

    db = SessionLocal()
    todo = Todo(task=data['task'])
    db.add(todo)
    db.commit()
    db.refresh(todo) # commit 자동 후 생성된 id 불러오기
    db.close()

    return jsonify({'id': todo.id, 'task' : todo.task}), 201

# UPDATE
@todo_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def put_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    if not todo:
        db.close()
        return jsonify({'error' : 'TODO NOT FOUND'}), 404
    data = request.get_json()
    todo.task = data['task']
    db.commit()
    updated = {'id': todo.id, 'task' : todo.task}
    db.close()
    return jsonify(updated), 200

# DELETE
@todo_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    if not todo:
        db.close()
        return jsonify({'error' : 'TODO NOT FOUND'}), 404
    db.delete(todo)
    db.commit()
    db.close()

    return jsonify({'deleted': todo_id})
