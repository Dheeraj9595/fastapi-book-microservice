from .database import database, s3_client, S3_BUCKET
from .models import books, BookIn
import json

async def add_book(payload: BookIn):
    query = books.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_books():
    query = books.select()
    return await database.fetch_all(query=query)


async def get_book(id):
    query = books.select(books.c.id == id)
    return await database.fetch_one(query=query)


# async def update_book(id: int, payload: BookIn):
#     query = books.update().where(books.c.id == id).values(**payload.dict())
#     return await database.execute(query=query)


async def update_book(book_id: int, payload: BookIn):
    # Update the book in the database
    query = books.update().where(books.c.id == book_id).values(**payload.dict())
    await database.execute(query=query)

    # Update the book in S3
    updated_book_data = {
        "book_id": book_id,
        **payload.dict()
    }
    json_data = json.dumps(updated_book_data)
    file_name = f'books/{book_id}.json'
    upload_to_s3(S3_BUCKET, file_name, json_data)

async def delete_book(id: int):
    query = books.delete().where(books.c.id == id)
    return await database.execute(query=query)

# Function to upload data to S3
def upload_to_s3(bucket_name, file_name, data):
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)