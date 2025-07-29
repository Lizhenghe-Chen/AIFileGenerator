from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    content: str = "如何追到喜欢的女生"
    userId: str = "666"
    expected_slides: Optional[int] = 4
    design_number: Optional[int] = 1
    filename: Optional[str] = "test"
