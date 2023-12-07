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
task_tag = Tag(name="Task", description="Visualização, adição e deleção de tarefas à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/tasks', tags=[task_tag], responses={"200": ListTasksSchema, "404": ErrorSchema})
def get_tasks():
    """Faz a busca por todas as Tasks cadastradas

    Retorna uma representação da listagem de tasks.
    """
    logger.debug(f"Coletando tasks ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tasks = session.query(Task).all()
    
    if not tasks:
        # se não há produtos cadastrados
        return {"tasks": []}, 200
    else:
        logger.debug(f"%d tasks encontradas" % len(tasks))
        # retorna a representação de task
        print(tasks)
        return show_tasks(tasks), 200

@app.post('/task', tags=[task_tag], responses={"200": TaskViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_task(form: TaskSchema):
    """Adiciona uma nova Task à base de dados.
    Retorna uma representação da task.
    """
    task = Task(
        description=form.description
    )
    logger.debug(f"Adicionando task: '{task.description}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando task
        session.add(task)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado task: '{task.description}'")
        return show_task(task), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar task '{task.description}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.route('/task/<int:task_id>', methods=['DELETE'])
def del_task(task_id: int):
    """Deleta uma Task a partir do id da task informada
    Retorna uma mensagem de confirmação da remoção.
    """
    print(task_id)
    logger.debug(f"Deletando dados sobre task #{task_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Task).filter(Task.id == task_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado task #{task_id}")
        return {"mesage": "Task removida", "id": task_id}
    else:
        # se a task não foi encontrada
        error_msg = "Task não encontrada na base :/"
        logger.warning(f"Erro ao deletar task #'{task_id}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.route('/task/<int:task_id>',  methods=['PUT'])
def update_task(task_id: int):
    """Atualiza uma Task a partir do id da task informada.
    Retorna uma representação atualizada da task.
    """
    logger.debug(f"Atualizando dados sobre task #{task_id}")
    session = Session()
    task = session.query(Task).filter(Task.id == task_id).first()

    if task:
        try:
            # Extract task status from JSON payload
            status = request.json.get('done')
            # Update task status
            task.done = status
            session.commit()
            logger.debug(f"Atualizada task #{task.id}")
            return show_task(task), 200
        except Exception as e:
            error_msg = "Não foi possível atualizar a task :/"
            logger.warning(f"Erro ao atualizar task #{task.id}, {error_msg}")
            return {"message": error_msg}, 400
    else:
        error_msg = "Task não encontrada na base :/"
        logger.warning(f"Erro ao atualizar task #{task.id}, {error_msg}")
        return {"message": error_msg}, 404