from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

""" 1:N 모델간의 관계 설명 """
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    todos = relationship('Todo', back_populates='user')

    def __repr__ (self):
        return f'<User(id={self.id}, name={self.name})>'
    
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='todos')

    def __repr__(self):
        return f'<Todo(id={self.id}, task={self.task})>'