import json
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/udacity_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='category', lazy=True)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def deleteTodo(todo_id):
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()

    return jsonify({
        'status': True,
        'message': 'Todo Deleted Successfully',
    })

@app.route('/todos/<todo_id>/alt-status', methods=['POST'])
def changeStatus(todo_id):
    status = json.loads(request.data)['status']
    todo = Todo.query.get(todo_id)
    todo.completed = status

    db.session.commit()
    
    return jsonify({
        'status': True,
        'message': 'Todo Status Change Successfully',
    })

@app.route('/todos/create', methods=['POST'])
def create():
    # description = request.form.get('description')
    body = json.loads(request.data)
    todo = Todo(description=body['description'], completed=False, category_id=body['category'])

    db.session.add(todo)
    db.session.commit()

    return jsonify({
        'status': True,
        'message': 'Todo Added Successfully',
        'data': {
            'id': todo.id,
            'description': todo.description
        }
    })

@app.route('/categories/<category_id>/todolist')
def getCategoryTodos(category_id):
    todoList = []
    categoriesList = Category.query.order_by('name').all()
    category = ''
    if(0):
        todoList = Todo.query.order_by('id')
    else:
        category = Category.query.get(category_id)
        todoList = Todo.query.filter_by(category_id=category_id).order_by('id')
    return render_template('index.html', todos=todoList.all(), categories=categoriesList, category=category)

@app.route('/')
def index():
    return redirect(url_for('getCategoryTodos', category_id=0))
    