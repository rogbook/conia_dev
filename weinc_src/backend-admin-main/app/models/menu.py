from pydantic import BaseModel
from typing import List, Dict, Optional


class DataMenu(BaseModel):
    id: int
    name: str
    depth: int
    menu_id: Optional[int]

    class Config:
        orm_mode = True


class DataMenuClass(BaseModel):
    class_code: str
    menu: DataMenu

    class Config:
        orm_mode = True
