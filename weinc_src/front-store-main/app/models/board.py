from typing import Optional

from pydantic import BaseModel


class AddComment(BaseModel):
    comment: str
    store_board_id: int
    store_code: Optional[str]
    ip: Optional[str]
