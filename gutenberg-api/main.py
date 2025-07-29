from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book, Author, Subject, Bookshelf, Format
from typing import List, Optional

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Gutenberg API is running!"}

@app.get("/books")
def get_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    mime_type: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    book_id: Optional[int] = Query(None),
    page: int = 1,
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    # Filter by ID
    if book_id:
        query = query.filter(Book.id == book_id)

    # Filter by title
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    # Filter by author name (case-insensitive partial match)
    if author:
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author}%"))

    # Filter by subject or bookshelf (topic)
    if topic:
        query = query.join(Book.subjects).join(Book.bookshelves).filter(
            (Subject.name.ilike(f"%{topic}%")) | (Bookshelf.name.ilike(f"%{topic}%"))
        )

    # Filter by mime type (file format)
    if mime_type:
        query = query.join(Book.formats).filter(Format.mime_type.ilike(f"%{mime_type}%"))

    # Sort by download_count descending
    query = query.order_by(Book.download_count.desc())

    # Pagination
    total = query.count()
    books = query.offset((page - 1) * 25).limit(25).all()

    # Build JSON response
    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "authors": [a.name for a in book.authors],
            "subjects": [s.name for s in book.subjects],
            "bookshelves": [b.name for b in book.bookshelves],
            "downloads": [
                {"mime_type": f.mime_type, "url": f.url} for f in book.formats
            ],
            "download_count": book.download_count,
        })

    return {
        "total": total,
        "page": page,
        "books": result
    }
