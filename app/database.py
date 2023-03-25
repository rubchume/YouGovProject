from typing import List, Dict

from pydantic import BaseModel
from sqlalchemy import func, create_engine, Column, String, SmallInteger, and_
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint


Base = declarative_base()


class VariableOption(BaseModel):
    variable_uuid: str
    variable_label: str
    variable_question: str
    variable_type: str
    answer_option: str
    answer_label: str
    answer_code: str


Base = declarative_base()


class VariableTaxonomy(Base):
    __tablename__ = 'variable_taxonomy'
    variable_uuid = Column(String, primary_key=True)
    variable_label = Column(String)
    variable_question = Column(String)
    variable_type = Column(String)
    answer_option = Column(String, primary_key=True)
    answer_label = Column(String)
    answer_code = Column(SmallInteger)


class Answers(Base):
    __tablename__ = 'answers'
    respondent_id = Column(String, primary_key=True)
    variable_uuid = Column(String, primary_key=True)
    value = Column(String)

    variable_taxonomy = relationship(
        "VariableTaxonomy",
        backref="answers",
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [variable_uuid, value],
            [VariableTaxonomy.variable_uuid, VariableTaxonomy.answer_option]
        ),
        {}
    )


engine = create_engine('sqlite:///app/data/example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_variable_options(variable_uuid) -> List[VariableOption]:
    options = session.query(VariableTaxonomy).filter(VariableTaxonomy.variable_uuid == variable_uuid).all()
    return [VariableOption(**option.__dict__) for option in options]


def get_variable_answers_counts(variable_uuid) -> Dict[int, int]:
    return dict(
        session
        .query(VariableTaxonomy.answer_code, func.count(Answers.value))
        .outerjoin(Answers)
        .filter(VariableTaxonomy.variable_uuid == variable_uuid)
        .group_by(VariableTaxonomy.answer_code)
        .all()
    )
