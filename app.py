from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify

from sqlalchemy.exc import IntegrityError

from model import Session, Task
from logger import logger
from schemas import *
from schemas.error import ErrorSchema
from schemas.task import *
from flask_cors import CORS

info = Info(title="ToDo List API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
task_tag = Tag(name="Task", description="Visualização, adição, atualização e deleção de tarefas na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/tasks', tags=[task_tag], responses={"200": ListTasksSchema, "404": ErrorSchema})
def get_tasks():
    """Faz a busca por todas as Tarefas cadastradas

    Retorna uma representação da listagem de tarefas.
    """
    logger.debug(f"Coletando tarefas ")
    session = Session()
    tasks = session.query(Task).all()
    
    if not tasks:
        return {"tasks": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tasks))
        print(tasks)
        return show_tasks(tasks), 200

@app.post('/task', tags=[task_tag], responses={"200": TaskViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_task(form: TaskSchema):
    """Adiciona uma nova Task à base de dados.
    Retorna uma representação da task.
    """
    # Validando que a string não está vazia
    if not form.description.strip():
        error_msg = "A tarefa não pode estar vazia."
        logger.warning(f"Erro ao adicionar tarefa: {error_msg}")
        return {"message": error_msg}, 400

    task = Task(
        description=form.description
    )
    logger.debug(f"Adicionando tarefa: '{task.description}'")
    try:
        session = Session()
        session.add(task)
        session.commit()
        logger.debug(f"Adicionado tarefa: '{task.description}'")
        return show_task(task), 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tarefa '{task.description}', {error_msg}")
        return {"message": error_msg}, 400

@app.patch('/task', tags=[task_tag], description="Atualiza o status de uma Tarefa a partir a partir do id e status.", responses={"200": TaskViewSchema, "404": ErrorSchema})
def update_task(form: TaskUpdateSchema):
    """Atualiza uma Tarefa a partir do id da tarefa informada e status.
    Retorna uma representação atualizada da tarefa.
    """
    task_id = form.id
    print("-------task_id = ${task_id}--------")
    logger.debug(f"Atualizando dados sobre tarefa #{task_id}")
    session = Session()
    task_db = session.query(Task).filter(Task.id == task_id).first()

    if task_db:
        try:
            done_value = form.done

            # Valida que o valor done_value seja 0 ou 1
            if done_value not in (0, 1):
                error_msg = "O valor de 'done' deve ser 0 ou 1."
                logger.warning(f"Erro ao atualizar tarefa #{task_db.id}, {error_msg}")
                return {"message": error_msg}, 400
            task_db.done = done_value
            session.commit()
            logger.debug(f"Atualizada tarefa #{task_db.id}")
            print(task_db)
            return show_task(task_db), 200
        except Exception as e:
            error_msg = "Não foi possível atualizar a tarefa :/"
            logger.warning(f"Erro ao atualizar tarefa #{task_db.id}, {error_msg}")
            return {"message": error_msg}, 400
    else:
        error_msg = "Tarefa não encontrada na base :/"
        logger.warning(f"Erro ao atualizar tarefa #{task_db.id}, {error_msg}")
        return {"message": error_msg}, 404
    
@app.delete('/task', tags=[task_tag], description="Remove uma Tarefa a partir a partir do id.", responses={"200": TaskDelSchema, "404": ErrorSchema})
def del_task(query: TaskSearchSchema):
    """Deleta uma Tarefa a partir do id da tarefa informada
    Retorna uma mensagem de confirmação da remoção.
    """
    task_id = query.id
    logger.debug(f"Deletando dados sobre task #{task_id}")
    session = Session()
    count = session.query(Task).filter(Task.id == task_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado tarefa #{task_id}")
        return {"message": "Tarefa removida", "id": task_id}
    else:
        error_msg = "Tarefa não encontrada na base :/"
        logger.warning(f"Erro ao deletar tarefa #'{task_id}', {error_msg}")
        return {"message": error_msg}, 404
