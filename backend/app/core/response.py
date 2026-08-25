from typing import Any, Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class ResponseEnvelope(BaseModel, Generic[DataT]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[DataT] = None
    error: Optional[dict] = None

class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int

class PaginatedData(BaseModel, Generic[DataT]):
    items: List[DataT]
    meta: PaginationMeta

def success_response(data: Any = None, message: str = "Operation completed successfully") -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "error": None
    }

def error_response(code: str, message: str, details: Optional[Any] = None) -> dict:
    return {
        "success": False,
        "message": message,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }
