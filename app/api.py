from typing import List, Dict

import fastapi

from fastapi import status, Path
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
    responses={
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"error": "Variable uuid '1234' was not found"}}}
        }
    }
)
def get_variable_options(variable_uuid: str = Path(title="Id of the variable", description="UUID of the variable", example="22d7bdb0-2172-11e4-813c-005056900044")):
    variable_options = database.get_variable_options(variable_uuid)

    if not variable_options:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Variable uuid '{variable_uuid}' was not found",
        )

    return variable_options_to_question_model(variable_options, variable_uuid)


def variable_options_to_question_model(variable_options, variable_uuid):
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


@app.get(
    "/variables/{variable_uuid}/counts",
    response_description="Answer counts",
    response_model=Dict[int, int],
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"error": "Variable uuid '1234' was not found"}}}
        }
    }
)
def get_variable_options(variable_uuid: str = Path(title="Id of the variable", description="UUID of the variable", example="22d7bdb0-2172-11e4-813c-005056900044")):
    counts = database.get_variable_answers_counts(variable_uuid)

    if not counts:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Variable uuid '{variable_uuid}' was not found",
        )

    return counts
