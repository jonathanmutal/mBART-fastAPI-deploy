from pydantic import BaseModel
from typing import List, Optional


class InputmBART(BaseModel):
    id: int
    input: List[str]
