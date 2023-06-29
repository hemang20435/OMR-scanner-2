from pydantic import BaseModel
from typing import List, Optional

class TestResult(BaseModel):
    name: str
    questions: List[str]
