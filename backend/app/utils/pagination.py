import math
from typing import Any, List

from pydantic import BaseModel

from app.config import settings


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    total_pages: int
    per_page: int


def paginate(query, page: int, per_page: int = None) -> dict:
    """Paginate a SQLAlchemy query and return structured response."""
    if per_page is None:
        per_page = settings.PAGE_SIZE

    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "per_page": per_page,
    }
