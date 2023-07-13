from fastapi import FastAPI, Depends
import schemas, models, database
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getdb():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def hash(password):
    return pwd_context.hash(password)

#user

@app.get('/user', tags=['user'])
def list_user(limit:int | None=None, db:Session=Depends(getdb)):
    if limit:
       users = db.query(models.User).limit(limit=limit).all()
    else:
       users = db.query(models.User).all()
    return users

@app.get('/user/{id}', tags=['user'])
def detail_user(id:int, db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    return user

@app.post('/user', tags=['user'])
def create_user(req:schemas.User, db:Session=Depends(getdb)):
    new_user = models.User(username=req.username, password=hash(req.password), email=req.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.put('/user/{id}', tags=['user'])
def update_user(id:int, req:schemas.User, db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.id == id)
    user.update({"username":req.username, "password":hash(req.password), "email":req.email})
    db.commit()
    return user.first()

@app.delete('/user/{id}', tags=['user'])
def delete_user(id:int, db:Session=Depends(getdb)):
    db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return "delete"

#blog

@app.get('/blog', tags=['blog'])
def list_blog(limit:int | None=None, db:Session=Depends(getdb)):
    if limit:
       blogs = db.query(models.Blog).limit(limit=limit).all()
    else:
       blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', tags=['blog'])
def detail_blog(id:int, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    return blog

@app.post('/blog', tags=['blog'])
def create_blog(req:schemas.Blog, db:Session=Depends(getdb)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@app.put('/blog/{id}', tags=['blog'])
def update_blog(id:int, req:schemas.Blog, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.update(req.dict())
    db.commit()
    return blog.first()

@app.delete('/blog/{id}', tags=['blog'])
def delete_blog(id:int, db:Session=Depends(getdb)):
    db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    return "delete"