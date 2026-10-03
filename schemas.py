from typing import Any, Dict

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    has_sale: bool = Field(False, description="Есть ли скидка")
    coffee_id: int = Field(..., ge=1, description="ID кофе (должен быть > 0)")
    address: Dict[str, Any] = Field(..., description="JSON-объект адреса")
