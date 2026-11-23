
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from .database import Base, engine, get_db
from . import models, schemas
from .security import hash_password, verify_password, create_access_token, decode_access_token

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="NEXUS Task Management API",
    description="A secure task management REST API with JWT authentication, SQLite persistence and validated CRUD endpoints.",
    version="1.0.0",
    contact={"name": "NEXUS API Project"}
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    subject = decode_access_token(token)
    if subject is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token",
                            headers={"WWW-Authenticate": "Bearer"})
    user = db.get(models.User, int(subject))
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user

@app.get("/", tags=["Health"])
def health_check():
    return {"service": "NEXUS Task Management API", "status": "online", "docs": "/docs"}

@app.post("/auth/register", response_model=schemas.UserOut, status_code=201, tags=["Authentication"])
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(models.User).where(
        (models.User.username == payload.username) | (models.User.email == payload.email)
    ))
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already registered")
    user = models.User(username=payload.username, email=payload.email,
                       password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/auth/login", response_model=schemas.TokenOut, tags=["Authentication"])
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.username == form.username))
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserOut, tags=["Users"])
def read_me(user: models.User = Depends(current_user)):
    return user

@app.post("/tasks", response_model=schemas.TaskOut, status_code=201, tags=["Tasks"])
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db),
                user: models.User = Depends(current_user)):
    task = models.Task(**payload.model_dump(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks", response_model=list[schemas.TaskOut], tags=["Tasks"])
def list_tasks(db: Session = Depends(get_db), user: models.User = Depends(current_user),
               task_status: str | None = Query(default=None, alias="status"),
               priority: str | None = Query(default=None),
               search: str | None = Query(default=None, min_length=1, max_length=80),
               skip: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100)):
    query = select(models.Task).where(models.Task.owner_id == user.id)
    if task_status:
        if task_status not in {"pending", "in_progress", "completed"}:
            raise HTTPException(status_code=422, detail="Invalid status filter")
        query = query.where(models.Task.status == task_status)
    if priority:
        if priority not in {"low", "medium", "high"}:
            raise HTTPException(status_code=422, detail="Invalid priority filter")
        query = query.where(models.Task.priority == priority)
    if search:
        query = query.where(models.Task.title.ilike(f"%{search}%"))
    query = query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(query).all())

@app.get("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    task = db.scalar(select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["Tasks"])
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db),
                user: models.User = Depends(current_user)):
    task = db.scalar(select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    task = db.scalar(select(models.Task).where(models.Task.id == task_id, models.Task.owner_id == user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None

@app.get("/analytics/summary", tags=["Analytics"])
def task_summary(db: Session = Depends(get_db), user: models.User = Depends(current_user)):
    tasks = list(db.scalars(select(models.Task).where(models.Task.owner_id == user.id)).all())
    return {
        "total": len(tasks),
        "pending": sum(t.status == "pending" for t in tasks),
        "in_progress": sum(t.status == "in_progress" for t in tasks),
        "completed": sum(t.status == "completed" for t in tasks),
        "high_priority": sum(t.priority == "high" for t in tasks)
                  }
  
