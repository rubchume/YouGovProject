from typing import List

import fastapi

from fastapi import status
from pydantic import BaseModel

from app import database

app = fastapi.FastAPI()


class OptionModel(BaseModel):
    code: int
    label: str
    option: str


class QuestionModel(BaseModel):
    label: str
    question: str
    options: List[OptionModel]
    type: str
    uuid: str


@app.get(
    "/variables/{variable_uuid}",
    response_description="Question details",
    response_model=QuestionModel,
    status_code=status.HTTP_200_OK,
)
def get_variable_options(variable_uuid: str):
    variable_options = database.get_variable_options(variable_uuid)

    if not variable_options:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Variable uuid '{variable_uuid}' was not found",
        )

    label = variable_options[0].variable_label
    question = variable_options[0].variable_question
    options = [
        dict(
            code=option.answer_code,
            label=option.answer_label,
            option=option.answer_option,
        )
        for option in variable_options
    ]
    variable_type = variable_options[0].variable_type

    return QuestionModel(
        label=label,
        question=question,
        options=options,
        type=variable_type,
        uuid=variable_uuid,
    )
