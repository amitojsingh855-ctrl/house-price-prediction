# import required SQLAlchemy
from sqlalchemy import Column, Integer,String

# import Base from base class
from database import Base

# create task table 
class Task(Base):

    # table name
    __tablename__ = "tasks"

    # Primary key
    id = Column(Integer , primary_key=True)

    # Task title
    task_title = Column(String , nullable=False)

    # Task description
    description = Column(String)

    # Employee Assigned
    assigned_to = Column(String)

    # Priority
    priority = Column(String)

    # Task status
    status = Column(String)

    # Due Date
    due_date = Column(String)

    # Created by 
    created_by = Column(String)

    # this file only defines the structure of the table , and think of it as a blueprint

    
