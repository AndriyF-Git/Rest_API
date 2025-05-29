from fastapi import APIRouter, HTTPException
from .schemas import Book, PyObjectId
from .database import books_collection
from bson import ObjectId

router = APIRouter()


@router.get("/books")
async def get_all_books():
    books = []
    cursor = books_collection.find({})
    async for doc in cursor:
        books.append(Book(**doc))
    return books


@router.get("/books/{book_id}")
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/books")
async def add_book(book: Book):
    book_dict = book.dict(by_alias=True)
    result = await books_collection.insert_one(book_dict)
    book_dict["_id"] = result.inserted_id
    return Book(**book_dict)


@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
