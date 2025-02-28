from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, security
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(security.verify_jwt)):
    user = db.query(models.User).filter(models.User.email == token["sub"]).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    return user


@app.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email = user.email.lower()

    db_user = crud.get_user_by_email(db, email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered"
        )
    
    return crud.create_user(db=db, user=user)


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):  
    db_user = crud.get_user_by_email(db, user.email.lower())
    
    if not db_user or not security.verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    
    access_token = security.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token}


@app.post("/tasks/create", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks", response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_tasks_by_id(db, current_user.id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, 
    task: schemas.TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    task_to_update = crud.get_tasks_by_id(db, task_id)
    
    if not task_to_update or task_to_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to update this task"
        )
    
    return crud.update_task(db=db, task_id=task_id, task=task)


@app.delete("/tasks/{task_id}", response_model=schemas.TaskOut)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    task_to_delete = crud.get_tasks_by_id(db, task_id)
    
    if not task_to_delete or task_to_delete.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this task"
        )
    
    return crud.delete_task(db=db, task_id=task_id)
