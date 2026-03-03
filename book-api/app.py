# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Create an instance of the FastAPI server
app = FastAPI(title = "Book Inventory API", version = "2.0.0")

# In-memory storage 
books: dict[int, "Book"] = {}

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    rating: Optional[float] = Field(default = None, le = 5.0, ge = 0.0)
    
class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int


@app.get("/books", response_model = list[Book])
async def get_books():
    return list(books.values())

@app.get("/books/{book_id}", response_model = Book)
async def get_book_by_id(book_id: int):
    if book_id not in books:
        raise HTTPException (status_code = 404, detail = f"Book with ID: {book_id} Not Found!")
    return books[book_id]
    

@app.post("/books", response_model = Book, status_code = 201)
async def publish_book(book: BookCreate):
    book_id = max(books.keys(), default = 0) + 1
    new_book = Book(id = book_id, **book.model_dump())
    books[book_id] = new_book
    return new_book

@app.put("/books/{book_id}", response_model = Book)
async def edit_book_by_id(book_id: int, updated_book: BookCreate):
    if book_id not in books:
        raise HTTPException (status_code = 404, detail = f"Book with ID: {book_id} Not Found!")
    updated = Book(id = book_id, **updated_book.model_dump())
    books[book_id] = updated
    return books[book_id]
    

@app.delete("/books/{book_id}", status_code = 204)
async def delete_book_by_id(book_id: int):
    if book_id not in books:
        raise HTTPException (status_code = 404, detail = f"Book with ID: {book_id} Not Found!")
    del books[book_id]    