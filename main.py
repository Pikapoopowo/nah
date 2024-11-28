from fastapi import FastAPI, Depands, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI
DATABASE_URL = "sqlite:///./todos.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal =sessionmaker(autocommit = False, autoflush = False, bind = engine)
# Define Model

class Todo(Base):
    _tablename_ = "todos"
    id = Column(Integer, primary = True, index = True)
    title = Column(String, nullable=True)
    completed = Column(Boolean, default = False)
# Initialize Database's Table
Base.metadara.creat_all(bind = engine)

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
class TodoCreat(TodoBase):
     pass
class TodoResponse(TodoBase):
     id: int
     class config:
          orm_dode = True
     
def get_db():
           db = SessionLocal()
           try:
                yield db
            finally:
                db.close()

@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depens(get_db)):
    return db.Query(Todo).all()

@app.get("/todos/{todo_id}", response_model = TodoResponse)
def read_todo(todo_id: int, db: Session = Depands(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
         raise HTTPException(status_code=404, details="Todo not found")
    return{db_todo}
@app.put("/todo/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
         raise HTTPException(status_code=404, details="Todo not found")
    for key, value in todo.dict().items():
         setattr(db_todo, key, value)
    db.commit()
    return{db_todo}
@app.delete("/todo/{todo_id}")
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
         raise HTTPException(status_code=404, details="Todo not found")
    db.delete(db_todo)
    db.commit()
    return{"detail":"Todo deleted successfully"}