from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

class MetaResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: MetaResponse

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: Optional[T] = None
    error: Optional[dict] = None
