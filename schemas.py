# import Basemodel
from pydantic import BaseModel


# task creation schema
class TaskSchema(BaseModel):

    # Task Title
    task_title : str

    # Task description
    description : str

    # employee assigned
    assigned_to  : str

    # priority
    priority : str

    status : str

    due_date : str

    created_by : str

    # this schema validates the data before it enter the cloud database 
