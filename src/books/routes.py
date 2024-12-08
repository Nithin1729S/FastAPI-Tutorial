from fastapi import APIRouter,HTTPException,status,Depends
from src.books.schemas import Book,BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional,List
from src.db.main import get_sessions
from src.books.service import BookService

book_router=APIRouter()
book_service=BookService()

@book_router.get("/",response_model=List[Book])
async def get_all_books(session:AsyncSession=Depends(get_sessions)):
    books=await book_service.get_all_books(session)
    return books

@book_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_data:Book,session:AsyncSession=Depends(get_sessions))->dict:
    new_book=await book_service.create_book(book_data,session)
    return new_book

@book_router.get("/{book_uid}")
async def get_book(book_uid: int,session:AsyncSession=Depends(get_sessions))->dict:
    book= await book_service.get_book(book_uid,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.patch("/{book_uid}")
async def update_book(book_uid: int,book_update_data:BookUpdateModel,session:AsyncSession=Depends(get_sessions))->dict:
    updated_book = await book_service.update_book(book_uid,book_update_data,session)
    if update_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: int,session:AsyncSession=Depends(get_sessions))->None:
    book_to_delete=await book_service.delete_book(book_uid,session)
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
