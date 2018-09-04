from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb'

mongo = PyMongo(app)

@app.route('/student', methods=['GET'])
def get_all_students():
  student = mongo.db.myCollection
  output = []
  for s in student.find():
    output.append({'student' : s['student'], 'id' : s['id'], 'number':s['number']})
  return jsonify({'result' : output})

@app.route('/student/find', methods=['POST'])
def get_one_student():
  stud = mongo.db.myCollection
  idd = request.json['id']
  s = stud.find_one({'id' : idd})
  if s:
    output = {'student' : s['student'], 'id' : s['id'], 'number' : s['number']}
  else:
    output = "No such student"
  return jsonify({'result' : output})

@app.route('/student/add', methods=['POST'])
def add_student():
  stud = mongo.db.myCollection
  student = request.json['student']
  idd = request.json['id']
  number = request.json['number']
  student_id = stud.insert({'student': student, 'id': idd, 'number':number})
  new_stud = stud.find_one({'_id': student_id })
  output = {'student' : new_stud['student'], 'id' : new_stud['id'], 'number' : new_stud['number']}
  return jsonify({'result' : output})

@app.route('/student/delete', methods=['POST'])
def delete_student():
  stud = mongo.db.myCollection
  idd = request.json['id']
  new_stud = stud.find_one({'id': idd })
  student_id = stud.delete_one({'id': idd})
  output = {'student' : new_stud['student'], 'id' : new_stud['id'], 'number' : new_stud['number']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
