from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"
# "postgresql://postgres:todo_password@localhost/todo_db"
Base = declarative_base()


class TodoItem(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    todos = relationship('TodoItem', back_populates='owner')


class UserCreate(BaseModel):
    username: str

class TodoItemCreate(BaseModel):
    task: str
    owner_id: int


TodoItem.owner = relationship('User', back_populates='todos')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.post('/users/')
def create_user(user: UserCreate):
    db = SessionLocal()
    with db as ses:
        db_user = User(username=user.username)
        ses.add(db_user)
        ses.commit()
        ses.refresh(db_user)
    return db_user


@app.post('/todos/')
def create_todo(item: TodoItemCreate):
    db = SessionLocal()
    db_item = TodoItem(task=item.task, owner_id=item.owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item


@app.get('/todos/{item_id}')
def read_todo(item_id: int):
    db = SessionLocal()
    item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.close()
    return item

