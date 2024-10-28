from sqlalchemy import Integer,String,Date,Column,func
from database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    department = Column(String)
    role = Column(String)
    date_joined = Column(Date,server_default=func.now())