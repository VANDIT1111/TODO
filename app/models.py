from sqlalchemy import Column,Integer,String
from app.database import declarative_base


Base = declarative_base()



class User:
    __tablename__ : 'users'
    
    id : Column(Integer, primary_key=True, nullable=False)
    username : Column(String, nullable=False)
    email : Column(String, nullable=False, unique=True)
    password_hash: Column(String, nullable=False)
    role: Column(String, nullable=False)
    
    
    
class Task:
    __tablename__ : 'tasks'
    id : Column(Integer, primary_key=True, nullable=False)
    title : Column(String, nullable=False)
    description : Column(String, nullable=False)
    status: Column(String, nullable=False)
    owner_id: Column(Integer, nullable= False)



