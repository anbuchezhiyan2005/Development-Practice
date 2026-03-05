# Learnings

## 1. How to add an entry in a Python dictionary?
To add an entry to a Python dictionary, use the following syntax:
```python
my_dict = {"name": "Alice", "age": 25}
my_dict["city"] = "New York"
print(my_dict)
```
Output:
```python
{'name': 'Alice', 'age': 25, 'city': 'New York'}
```

## 2. How to create a dictionary like `{"ID": 1, "Book": Book}`?
```python
my_dict = {"ID": 1, "Book": "Book"}
```
If `Book` is a variable:
```python
Book = "Harry Potter"
my_dict = {"ID": 1, "Book": Book}
```
Output:
```python
{'ID': 1, 'Book': 'Harry Potter'}
```

## 3. How to remove an entry from a dictionary?
Use `del` or `pop()`:
```python
# Using del
del books[1]

# Using pop()
removed_entry = books.pop(1, None)
```

## 4. Will removing an entry mess with the ID order?
Yes, deleting an entry will leave gaps in the sequence of IDs. For example:
```python
books = {1: {...}, 2: {...}, 3: {...}}
del books[2]
print(books)  # {1: {...}, 3: {...}}
```
IDs will no longer be sequential. Reordering IDs is possible but not recommended for production systems.

## 5. What is the structure of the following code?
```python
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
```
### Explanation:
- `BookBase`: Base class defining shared fields.
- `BookCreate`: Inherits `BookBase` and is used for client input.
- `Book`: Inherits `BookBase` and adds an `id` field for server responses.

## 6. Why is the second approach cleaner?
```python
# Overly nested
books[book_id] = {"ID": book_id, "Book": book}

# Cleaner
books[book_id] = Book(id=book_id, **book.model_dump())
```
### Explanation:
- The second approach avoids unnecessary nesting and redundancy.
- It directly stores the `Book` object, making the structure flat and easier to work with.

## 7. What does `**` do in Python?
The `**` operator is used for dictionary unpacking. It passes key-value pairs as keyword arguments.
Example:
```python
data = {"title": "1984", "author": "George Orwell"}
book = Book(**data)
```
Equivalent to:
```python
book = Book(title="1984", author="George Orwell")
```

## 8. Will `model_dump()` help in updating `Book` objects without creating a new one?
Yes, `model_dump()` converts a Pydantic model into a dictionary, which can be updated and used to recreate the object.
Example:
```python
book_data = book.model_dump()
updated_data = {"title": "Animal Farm"}
book_data.update(updated_data)
book = Book(**book_data)
```

## 9. Why do I need `.items()`? Why not just `model_dump()`?
`.items()` is needed to access both keys and values of the dictionary returned by `model_dump()`. Without `.items()`, you can only iterate over the keys.
Example:
```python
updated_data = {k: v for k, v in book.model_dump().items() if v is not None}
```

## 10. What is automatic serialization safety?
Serialization converts Python objects into formats like JSON for transmission. FastAPI ensures:
- The response matches the `response_model`.
- Extra fields or sensitive data are excluded.
Example:
```python
@app.get("/books", response_model=Book)
async def get_book():
    return BookInternal(id=1, title="1984", internal_id=123)
```
The `internal_id` field will be excluded from the response.

## 11. What does "serialization" mean?
Serialization is the process of converting an object into a format (e.g., JSON) that can be stored or transmitted. Deserialization is the reverse process.
Example:
```python
import json
book = {"title": "1984", "author": "George Orwell"}
serialized = json.dumps(book)  # Serialize to JSON
print(serialized)  # {"title": "1984", "author": "George Orwell"}
```

## 12. Will the `Book` objects from the dictionary be automatically retrieved and compiled into a list?

No, the `response_model=list[Book]` in the `@app.get("/books")` endpoint specifies that the output should be a **list of `Book` objects**, but the `books` dictionary must be explicitly converted into a list. FastAPI does not automatically retrieve and compile the dictionary values into a list.

### Correct Implementation:
To ensure the response matches the `response_model`, extract the values from the dictionary and return them as a list:
```python
@app.get("/books", response_model=list[Book])
async def get_books():
    return list(books.values())  # Extract dictionary values and convert to a list
```

### Explanation:
1. **`books.values()`**:
   - Retrieves all the values (i.e., the `Book` objects) from the `books` dictionary.
   - Example:
     ```python
     {
         1: Book(id=1, title="1984", author="George Orwell", year=1949, rating=4.8),
         2: Book(id=2, title="Animal Farm", author="George Orwell", year=1945, rating=4.5)
     }
     ```
     `books.values()` will return:
     ```python
     [
         Book(id=1, title="1984", author="George Orwell", year=1949, rating=4.8),
         Book(id=2, title="Animal Farm", author="George Orwell", year=1945, rating=4.5)
     ]
     ```

2. **`list(books.values())`**:
   - Converts the `dict_values` object returned by `books.values()` into a list, which matches the `response_model=list[Book]`.

### What Happens Internally:
1. **Validation**:
   - FastAPI validates the returned list of `Book` objects against the `response_model=list[Book]`.
   - If any object in the list does not conform to the `Book` model (e.g., missing fields, incorrect types), FastAPI raises a validation error.

2. **Serialization**:
   - FastAPI serializes the list of `Book` objects into JSON before sending it to the client.

### Example Response:
If the `books` dictionary contains:
```python
{
    1: Book(id=1, title="1984", author="George Orwell", year=1949, rating=4.8),
    2: Book(id=2, title="Animal Farm", author="George Orwell", year=1945, rating=4.5)
}
```
The client will receive the following JSON response:
```json
[
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "rating": 4.8
    },
    {
        "id": 2,
        "title": "Animal Farm",
        "author": "George Orwell",
        "year": 1945,
        "rating": 4.5
    }
]
```

## 13. Is the `publish_book` endpoint correctly matched to the `response_model`?

### Issue:
The `publish_book` endpoint specifies `response_model=Book`, which means the response should be a **single `Book` object**. However, the original code returns a dictionary with extra fields:
```python
return {"message": "Book published!", "Book": book}
```
This does not match the `response_model` and will cause a validation error.

### Correct Implementation:
To match the `response_model=Book`, the function should return the `Book` object directly:
```python
@app.post("/books", response_model=Book, status_code=201)
async def publish_book(book: BookBase):
    book_id = max(books.keys(), default=0) + 1
    new_book = Book(id=book_id, **book.model_dump())  # Create the Book object
    books[book_id] = new_book  # Store it in the dictionary
    return new_book  # Return the Book object directly
```

### Why This Fix Works:
1. **`response_model=Book`**:
   - The `response_model` specifies that the response should be a `Book` object.
   - By returning `new_book` (a `Book` object), the response matches the `response_model`.

2. **Serialization**:
   - FastAPI automatically serializes the `Book` object into JSON before sending it to the client.
   - For example, if the `Book` object is:
     ```python
     Book(id=1, title="1984", author="George Orwell", year=1949, rating=4.8)
     ```
     The client will receive:
     ```json
     {
         "id": 1,
         "title": "1984",
         "author": "George Orwell",
         "year": 1949,
         "rating": 4.8
     }
     ```

3. **No Extra Fields**:
   - The corrected code ensures that only the fields defined in the `Book` model are included in the response. The `"message"` field is removed because it is not part of the `Book` model.

### What Happens If You Don't Fix It?
If you return the dictionary `{"message": "Book published!", "Book": book}` instead of the `Book` object:
1. **Validation Error**:
   - FastAPI will validate the response against the `response_model=Book`.
   - Since the response is a dictionary with extra fields (`"message"` and `"Book"`), FastAPI will raise a validation error.

2. **Error Example**:
   - The client will receive a `500 Internal Server Error` with a message like:
     ```json
     {
         "detail": [
             {
                 "loc": ["response"],
                 "msg": "value is not a valid dict",
                 "type": "type_error.dict"
             }
         ]
     }
     ```

## 14. Why is the Pydantic validation for the `Book` object given in double quotes and not the `int`?

### Code:
```python
books: dict[int, "Book"] = {}
```

### Explanation:
1. **Forward Reference**:
   - The `Book` class is defined **after** this line in the code. At the time Python parses this line, the `Book` class has not yet been fully defined.
   - To avoid a `NameError`, the type hint for `Book` is written as a **string** (`"Book"`). This is called a **forward reference**.

2. **Why `int` Doesn't Need Quotes**:
   - `int` is a built-in type in Python and is always recognized by the interpreter. It does not depend on the order of definitions, so it does not need to be enclosed in quotes.

### How Forward References Work:
In Python, when you use a type hint for a class that hasn't been defined yet, you can use a string to refer to the class. This tells Python to resolve the type later, after the class is defined.

Example:
```python
# Forward reference for Book
books: dict[int, "Book"] = {}

class Book:
    id: int
    title: str
```
Here, `"Book"` is resolved after the `Book` class is defined.

---

## 15. Is there any problem with the path parameter in the `get_book_by_id` endpoint?

### Problem:
The path parameter name in the route (`/books/{id}`) does not match the function argument name (`book_id`). This mismatch will cause FastAPI to raise an error when trying to call the endpoint.

### Incorrect Code:
```python
@app.get("/books/{id}", response_model=Book)
async def get_book_by_id(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"Book with ID: {book_id} Not Found!")
    return books[book_id]
```

### Why This Is a Problem:
- FastAPI uses the **path parameter name** to map the value from the URL to the corresponding **function argument**.
- If the names do not match, FastAPI cannot pass the value to the function, and you'll encounter an error.

### Solution:
The **path parameter name** in the route must match the **function argument name**. You can fix this by renaming either the path parameter or the function argument.

#### Option 1: Change the Path Parameter to Match the Function Argument
```python
@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"Book with ID: {book_id} Not Found!")
    return books[book_id]
```

#### Option 2: Change the Function Argument to Match the Path Parameter
```python
@app.get("/books/{id}", response_model=Book)
async def get_book_by_id(id: int):
    if id not in books:
        raise HTTPException(status_code=404, detail=f"Book with ID: {id} Not Found!")
    return books[id]
```

### Best Practice:
To avoid confusion, it’s a good idea to keep the path parameter name and the function argument name consistent. For example:
```python
@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"Book with ID: {book_id} Not Found!")
    return books[book_id]
```

## 16. What do the packages `sqlalchemy`, `psycopg2-binary`, and `python-dotenv` do?
- **`sqlalchemy`**: A Python SQL toolkit and ORM library for interacting with databases in a Pythonic way.
- **`psycopg2-binary`**: A PostgreSQL database adapter for Python, allowing connections to PostgreSQL databases.
- **`python-dotenv`**: A package to manage environment variables by loading them from a `.env` file.

## 17. What does the Docker command for PostgreSQL do?
### Command:
```bash
docker run --name books-db \\\n  -e POSTGRES_USER=admin \\\n  -e POSTGRES_PASSWORD=secret \\\n  -e POSTGRES_DB=booksdb \\\n  -p 5432:5432 \\\n  -d postgres
```
### Explanation:
- Creates and runs a PostgreSQL database container named `books-db`.
- Sets environment variables for the database: user (`admin`), password (`secret`), and database name (`booksdb`).
- Maps port `5432` on the host to port `5432` in the container.
- Runs the container in detached mode using the official `postgres` image.

## 18. What is the usual port number for databases in work environments?
- **PostgreSQL**: `5432`
- **MySQL/MariaDB**: `3306`
- **Microsoft SQL Server**: `1433`
- **Oracle Database**: `1521`
- **MongoDB**: `27017`
- **Redis**: `6379`
- **Elasticsearch**: `9200`

## 19. How to span a command across multiple lines?
- Use a backslash (`\\`) at the end of each line in Unix-like shells (e.g., Bash):
  ```bash
  docker run --name books-db \\\n    -e POSTGRES_USER=admin \\\n    -e POSTGRES_PASSWORD=secret \\\n    -e POSTGRES_DB=booksdb \\\n    -p 5432:5432 \\\n    -d postgres
  ```
- Use a caret (`^`) in Windows Command Prompt:
  ```cmd
  docker run --name books-db ^\n    -e POSTGRES_USER=admin ^\n    -e POSTGRES_PASSWORD=secret ^\n    -e POSTGRES_DB=booksdb ^\n    -p 5432:5432 ^\n    -d postgres
  ```
- Use a backtick (`` ` ``) in PowerShell:
  ```powershell
  docker run --name books-db `\n    -e POSTGRES_USER=admin `\n    -e POSTGRES_PASSWORD=secret `\n    -e POSTGRES_DB=booksdb `\n    -p 5432:5432 `\n    -d postgres
  ```

## 20. What does the error "failed to connect to the Docker API at npipe:////./pipe/dockerDesktopLinuxEngine" mean?
- **Cause**: Docker cannot connect to the Linux container engine.
- **Fixes**:
  1. Ensure Docker Desktop is running.
  2. Switch to the correct container engine (Linux or Windows).
  3. Restart Docker Desktop.
  4. Reinstall Docker Desktop if necessary.

## 21. How to verify a running Docker container?
- Use `docker ps` to list running containers.
- Access the container shell: `docker exec -it books-db bash`.
- Connect to the PostgreSQL database: `docker exec -it books-db psql -U admin -d booksdb`.
- View logs: `docker logs books-db`.
- Stop the container: `docker stop books-db`.
- Restart the container: `docker start books-db`.

---

## 22. What is a generator in Python?
- A **generator** is a special type of iterable that produces values lazily, meaning it generates values one at a time as needed, rather than computing and storing them all at once in memory.
- Generators are created using functions with the `yield` keyword.

### Key Features:
1. **Lazy Evaluation**: Generates values on demand, making it memory-efficient.
2. **State Retention**: Retains its state between calls, resuming execution from where it left off.
3. **One-Time Iteration**: Can only be iterated once; after exhaustion, it cannot be reused.

### Example:
```python
def my_generator():
    print("First value")
    yield 1
    print("Second value")
    yield 2
    print("Third value")
    yield 3
```

### Difference Between `yield` and `return`:
- **`yield`**: Pauses the function and allows it to resume later, producing multiple values over time.
- **`return`**: Ends the function and returns a single value.

---

## 23. How does `get_session()` work in SQLAlchemy?
The `get_session()` function is a utility to manage the lifecycle of a database session.

### Code:
```python
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

### Explanation:
1. **Session Creation**:
   - `SessionLocal()` creates a new session instance to interact with the database.
2. **`yield session`**:
   - The `yield` keyword provides the session to the caller (e.g., a FastAPI route) for temporary use.
3. **Session Cleanup**:
   - The `finally` block ensures the session is closed after use, releasing the database connection back to the pool.

### Why Use `get_session()`?
- **Isolation**: Each request gets its own session, preventing interference between requests.
- **Resource Management**: Ensures sessions are properly closed, avoiding connection leaks.
- **Transaction Safety**: Each session operates within its own transaction, allowing rollbacks on errors.

---

## 24. How many `Session` instances can be created?
The number of `Session` instances depends on the **connection pool size** and the **database server's capacity**.

### Connection Pool in SQLAlchemy:
- **Default Pool Size**: 5 connections.
- **Behavior When Full**: If all connections are in use, SQLAlchemy waits for a connection to become available (default timeout: 30 seconds).

### Scaling for Many Users:
You can adjust the connection pool size when creating the engine:
```python
engine = create_engine(\n    DATABASE_URL,\n    echo=True,\n    pool_size=20,         # Maximum number of connections in the pool\n    max_overflow=10,      # Additional connections allowed beyond the pool size\n    pool_timeout=30,      # Time (in seconds) to wait for a connection\n)\n```

### Database Server Limits:
- **PostgreSQL**: Default limit is 100 connections.
- **MySQL**: Default limit is 151 connections.

### Handling High Traffic:
1. **Optimize Queries**: Minimize database queries per request.
2. **Increase Pool Size**: Adjust `pool_size` and `max_overflow` to handle more concurrent sessions.
3. **Database Scaling**: Use read replicas or sharding to distribute the load.
4. **Connection Management**: Ensure sessions are closed promptly after use.

---

### Summary:
- Generators are memory-efficient and stateful iterables.
- `get_session()` ensures proper session management for database interactions.
- Connection pool size and database limits determine how many sessions can be created.

These concepts are essential for building scalable and efficient database-driven applications.
