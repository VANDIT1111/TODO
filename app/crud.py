from sqlalchemy.orm import Session 
from app import models, schemas, security
 

def create_user(db: Session, user: schemas.UserCreate): 
    db_user =models.User(username=user.username, email=user.email, password_hash=security.get_password_hash(user.password), role=user.role) 
    db.add(db_user) 
    db.commit() 
    db.refresh(db_user) 
    return db_user 

def get_user_by_email(db: Session, email: str): 
    return db.query(models.User).filter(models.User.email == email).first() 

def create_task(db: Session, task: schemas.TaskCreate, user_id: int): 
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id) 
    db.add(db_task) 
    db.commit() 
    db.refresh(db_task) 
    return db_task 

def get_tasks_by_user(db: Session, user_id: int): 
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all() 

def get_all_tasks(db: Session): 
    return db.query(models.Task).all() 

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate): 
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first() 
    if db_task: db_task.title = task.title 
    db_task.description = task.description 
    db_task.status = task.status 
    db.commit() 
    db.refresh(db_task) 
    return db_task 

def delete_task(db: Session, task_id: int): 
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first() 
    if db_task: 
        db.delete(db_task) 
        db.commit() 
    return db_task