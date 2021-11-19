from flask import Flask, jsonify, request
from flask_pymongo import  PyMongo, ObjectId
from os import environ

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/subcategorias"
mongo = PyMongo(app)
db = mongo.db


@app.route('/api/subcategoria/<subcategoria_id>', methods=['GET'])
def getTodo(todo_id):
    _todo = db.todo.find_one({"_id": ObjectId(todo_id)})
    item = {
        'id': str(_todo['_id']),
           'name': _todo['name']
    }

    return jsonify(data=item), 200


@app.route('/api/subcategoria', methods=['GET'])
def getTodos():
    _todos = db.todo.find()
    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'name': todo['name']
        }
        data.append(item)

    return jsonify(data=data), 200


@app.route('/api/subcategoria', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
              'name': data['name']
    }
    db.todo.insert_one(item)

    return jsonify(data=data), 201




@app.route('/api/subcategoria/<subcategoria_id>', methods=['PATCH'])
def updateTodo(todo_id):
    data = request.get_json(force=True)
    db.todo.update_one({"_id": ObjectId(todo_id)}, {"$set": data})

    return jsonify(data=data), 204


@app.route('/api/subcategoria/<subcategoria_id>', methods=['DELETE'])
def deleteTodo(todo_id):
    db.todo.delete_one({"_id": ObjectId(todo_id)})

    return jsonify(), 204


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
