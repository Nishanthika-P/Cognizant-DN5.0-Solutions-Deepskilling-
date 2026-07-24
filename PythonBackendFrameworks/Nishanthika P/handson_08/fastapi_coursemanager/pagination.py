"""
pagination.py
Hands-On 8, Task 2, step 83: DRF-style offset pagination envelope.
"""
from typing import Optional
from pydantic import BaseModel


class Page(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list


def build_page(items, total_count, request, page, page_size) -> Page:
    base_url = str(request.url).split('?')[0]

    next_url = None
    if page * page_size < total_count:
        next_url = f'{base_url}?page={page + 1}&page_size={page_size}'

    previous_url = None
    if page > 1:
        previous_url = f'{base_url}?page={page - 1}&page_size={page_size}'

    return Page(count=total_count, next=next_url, previous=previous_url, results=items)
