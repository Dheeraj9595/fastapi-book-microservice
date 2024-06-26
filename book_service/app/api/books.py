from typing import List
from fastapi import APIRouter, HTTPException
from .service import fetch_author

from . import db_manager
from .service import is_author_present
from .models import BookIn, BookOut, BookUpdate

books = APIRouter()


# @books.get("/", response_model=List[BookOut], status_code=200)
# async def list_book() -> dict:
#     """
#     Fetch all books
#     """
#     return await db_manager.get_all_books()

# db_manager = {
#     "get_all_books": db_manager.get_all_books,
# }

@books.get("/", response_model=List[BookOut], status_code=200)
async def list_book():
    """
    Fetch all books
    """
    books = await db_manager.get_all_books()
    book_list = []

    # Collect all author IDs from all books
    all_author_ids = {author_id for book in books for author_id in book["authors_id"]}

    # Fetch author details for all collected author IDs
    author_details = {}
    for author_id in all_author_ids:
        try:
            author = await fetch_author(author_id)
            author_details[author_id] = author.author_name
        except HTTPException as e:
            if e.status_code == 404:
                author_details[author_id] = f"Author with id {author_id} not found"
            else:
                raise

    for book in books:
        book_dict = dict(book)
        authors = [author_details[author_id] for author_id in book_dict["authors_id"]]
        book_dict["authors"] = authors
        book_list.append(book_dict)

    return book_list

@books.get("/{book_id}", response_model=BookOut, status_code=200)
async def get_book(book_id: int):
    """
    Fetch a single book by ID
    """
    book = await db_manager.get_book(book_id)
    if not book:
        HTTPException(status_code=404, detail="Book not found")
    return book


@books.post("/create/", response_model=BookOut, status_code=201)
async def create_book(payload: BookIn):
    """
    Create a book
    """
    for author_id in payload.authors_id:
        if not is_author_present(author_id):
            raise HTTPException(
                status_code=404,
                detail=f"Author with id:{author_id} not found")

    book_id = await db_manager.add_book(payload)
    response = {"id": book_id, **payload.dict()}
    return response



@books.put("/update/{book_id}/", response_model=BookOut)
async def update_book(book_id: int, payload: BookUpdate):
    book = await db_manager.get_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = payload.dict(exclude_unset=True)
    if "authors_id" in update_data:
        for author_id in update_data["authors_id"]:
            if not is_author_present(author_id):
                breakpoint()
                raise HTTPException(
                    status_code=404,
                    detail=f"Author with id:{author_id} not found"
                )

    book_id_db = BookIn(**book)
    update_book = book_id_db.copy(update=update_data)
    await db_manager.update_book(book_id, update_book)
    updated_book = await db_manager.get_book(book_id)
    return updated_book


@books.delete("/delete/{book_id}/", response_model=None)
async def delete_book(book_id: int):
    book = await db_manager.get_book(book_id)
    if not book:
        HTTPException(status_code=404, detail="Book not found")
    return await db_manager.delete_book(book_id)
