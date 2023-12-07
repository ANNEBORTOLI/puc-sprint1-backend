from pydantic import BaseModel
from typing import Optional, List
from model.task import Task

class TaskSchema(BaseModel):
    """ Define como uma nova task a ser inserida deve ser representada
    """
    description: str = "Marcar nutricionista"

class TaskUpdateSchema(BaseModel):
    """ Define como uma task a ser editada deve ser representada
    """
    id: int = 1
    done: int = 1

class TaskSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no id da task.
    """
    id: int = 1

class ListTasksSchema(BaseModel):
    """ Define como uma listagem de tasks será retornada.
    """
    tasks:List[TaskSchema]

def show_tasks(tasks: List[Task]):
    """ Retorna uma representação da task seguindo o schema definido em
        TaskViewSchema.
    """
    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "description": task.description,
            "done": task.done,
        })

    return {"tasks": result}

class TaskViewSchema(BaseModel):
    """ Define como uma task será retornada: task.
    """
    id: int = 1
    description: str = "Cortar cabelo",
    done: Optional[int] = 0

class TaskDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    description: str

def show_task(task: Task):
    """ Retorna uma representação do produto seguindo o schema definido em TaskViewSchema.
    """
    return {
        "id": task.id,
        "description": task.description,
        "done": task.done,
    }
