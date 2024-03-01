from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    question: str
    answer: Optional[str] = None
