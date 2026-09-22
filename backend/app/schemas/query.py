from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def strip_and_check_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be blank")
        return v

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
