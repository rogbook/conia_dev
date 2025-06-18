from pydantic import BaseModel
from typing import List, Dict, Optional


class DataPermission(BaseModel):
    code: str
    name: str
    description: Optional[str]
    type: Optional[str]
    category: Optional[str]
    group: Optional[str]
    exclude: Optional[str]

    class Config:
        orm_mode = True


class DataMemberPermission(BaseModel):
    permissions: List[Dict[str, str]]
