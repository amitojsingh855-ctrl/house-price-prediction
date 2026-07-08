from fastapi import FastAPI , Depends
# updated as per Day_2

from sqlalchemy.orm import Session
# updated code as per Day2

from database import get_db
# updated code as per Day2

from schemas import TaskSchema
# updated code as per Day2


from database import Base , engine

from models import Task

Base.metadata.create_all(bind = engine)


# here Base contains all database table definition
# and engine , contains the cloud database connection

app = FastAPI()


# Home endpoint 
@app.get("/")
def home():

    return {"message" : "Welcome to Cloud Task Manager API"}


# This API  tells that : FastAPI is running and the application started successfully

# now run the project using uvicorn main: app --reload 


# As per Day_2

@app.post("/create_task")
def create_task(task : TaskSchema , db : Session= Depends(get_db)):

    # create task object
    new_task = Task(task_title = task.task_title , description = task.description,assigned_to = task.assigned_to,priority = task.priority , status = task.status ,due_date = task.due_date,created_by = task.created_by)


    # add task
    db.add(new_task)

    # commit changes
    db.commit()

    # refresh object
    db.refresh(new_task)

    # return response
    return {"message" : "Task Created Successfully"}

# the data sent from Postman is first validated by the Taskschema (Pydantic schema) , if it is valid , the values are then copied into the task model , which represents the database table , and finally stored in the database 

# now , go to the postman and start implementing the operations

@app.get("/tasks")
def get_task(db = Depends(get_db)):


    tasks = db.query(Task).all()


    return tasks
