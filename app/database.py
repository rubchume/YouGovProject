from typing import List

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, SmallInteger, ForeignKey, and_
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class VariableOption(BaseModel):
    variable_uuid: str
    variable_label: str
    variable_question: str
    variable_type: str
    answer_option: str
    answer_label: str
    answer_code: str


class VariableTaxonomy(Base):
    __tablename__ = 'variable_taxonomy'
    variable_uuid = Column(String, primary_key=True)
    variable_label = Column(String)
    variable_question = Column(String)
    variable_type = Column(String)
    answer_option = Column(String, primary_key=True)
    answer_label = Column(String)
    answer_code = Column(SmallInteger)

    # answers = relationship("Answers", back_populates="variable_taxonomy")


class Answers(Base):
    __tablename__ = 'answers'
    respondent_id = Column(String, primary_key=True)
    variable_uuid = Column(String, ForeignKey('variable_taxonomy.variable_uuid'), primary_key=True)
    value = Column(String, ForeignKey('variable_taxonomy.answer_option'))

    variable_taxonomy = relationship(
        "VariableTaxonomy",
        # back_populates="answers",
        primaryjoin=and_(
            VariableTaxonomy.variable_uuid == variable_uuid,
            VariableTaxonomy.answer_option == value
        )
    )


engine = create_engine('sqlite:///app/data/example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_variable_options(variable_uuid) -> List[VariableOption]:
    options = session.query(VariableTaxonomy).filter(VariableTaxonomy.variable_uuid == variable_uuid).all()
    return [VariableOption(**option.__dict__) for option in options]
