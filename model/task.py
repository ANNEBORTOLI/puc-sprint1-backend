from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Task(Base):
    __tablename__ = 'task'

    id = Column("pk_task", Integer, primary_key=True)
    description = Column(String(140))
    done = Column(Integer, default=0)
    insertion_date = Column(DateTime, default=datetime.now())

    def __init__(self, description:str, done:int = 0,
                 insertion_date:Union[DateTime, None] = None):
        """
        Cria um Task

        Arguments:
            description: descrição da Task.
            dane: se a Task foi concluída(true) ou não(false)
            insertion_date: data de quando o Task foi inserida à base
        """
        self.description = description
        self.done = done

        # se não for informada, será o data exata da inserção no banco
        if insertion_date:
            self.insertion_date = insertion_date

