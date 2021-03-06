from flask import Flask
from flask import jsonify
from flask import request
from flask import Response,make_response
from flask_cors import CORS
from flask_pymongo import PyMongo
import pdb

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb'
CORS(app, resources=r'/*') #跨域请求
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
  data = request.json
  stud = mongo.db.myCollection
  idd = data['id']
  s = stud.find_one({'id' : idd})
  print(s)
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

@app.route('/student/modify', methods=['POST'])
def modify_one_student():
  stud = mongo.db.myCollection
  student = request.json['student']
  number = request.json['number']
  modify_id = request.json['id'] #需修改的学生id
  s = stud.find_one({'id' : modify_id})
  if s:
    stud.update_one(
      {"id" : modify_id},
      {"$set":{"student" : student, "number" : number}}
    )
    output = {'student' : student, 'id' : modify_id, 'number' : number}
    
  else:
    output = "No such student"
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(
      host = '192.168.147.149',
        port = 7777,  
        debug = True )
