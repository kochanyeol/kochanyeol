from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# 파이썬에서 DB를 다루는 다이어리 SQL을 직접 쓰지 않고 파이썬에서 DB를 다룸
# create_engine은 DB와 실제로 연결해주는 엔진(규칙)
# Column은 테이블의 컬럼(열)을 만들기위해 사용
# INT,STR은 컬럼의 데이터 타입을 지정하기 위해 사용
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
# orm은 DB의 테이블,행과 파이썬의 클래스,객체를 연결
# declarative_base는 관계형 데이터베이스의 테이블을 파이썬 객체(클래스)로 매핑하여 SQL 없이 객체처럼 데이터를 다룰 수 있게 해주는 기술
# create_engine이걸로 DB와 연결을 했으면 sessionmaker이걸로 DB와 작업통로를 찍어낸다.
import os

app = Flask(__name__)

""" DB 설정 """
BASE_DIR = os.path.dirname(__file__)
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(INSTANCE_DIR, 'todos.db')}"
engine = create_engine(DATABASE_URL, echo=True)
# echo=True는 DB에 실제로 보낸 SQL명령을 터미널에 그대로 출력해주는 옵션 쉽게말해
# VSCODE에서 터미널을 통해 코드를 실행시키면 실행된 명령어를 터미널에 출력해주는 것

SessionLocal = sessionmaker(bind=engine)

""" 모델 정의 """

Base = declarative_base()
# ORM 모델을 정의하기 위한 공통 부모 클래스(Base)를 생성하는 함수
# 이 Base를 상속받는 클래스는 전부 DB 테이블이다.
class User(Base):
# 이 클래스는 orm테이블이다 선언.
    __tablename__ = 'users'
    # MODEL 정의하기

    id = Column(Integer, primary_key=True, index=True)
    # index=True는 검색 속도 향상용 인덱스를 생성하는 것
    name = Column(String, nullable=False)
    # nullable=False == not null

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name})>'
    # repr은 디버깅용으로 없다면 <__main__.User object at 0x000001F...>으로 보일것이고,
    # 있다면 <User(id=1, name=OZ_BE)>로 보인다

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='todos')
    # 유저 테이블과 todo 테이블의 1:N관계 형성

    def __repr__(self):
        return f'<Toto(id={self.id}, task={self.task})>'


Base.metadata.create_all(bind=engine)
# Base.metadata는 Base를 상속 받은 모든 orm모델(class=db) 즉 테이블,컬럼,제약조건 등의 구조 정보를 담음

# READ: 전체 항목 조회  
@app.route('/')
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return jsonify([{'id':t.id, 'task':t.task} for t in todos]), 200

# CREATE
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    db.close()
    if not todo:
        return jsonify({'error' : '에러발생'}), 404
    return jsonify({'id' : todo.id, 'task' : todo.task}), 200
    
# READ
@app.route('/todos', methods=['POST'])
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
@app.route('/todos/<int:todo_id>', methods=['PUT'])
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
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
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

if __name__ == '__main__':
    app.run(debug=True)