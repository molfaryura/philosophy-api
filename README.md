# Philosophy API

The Philosophy API is a Flask-based web application that allows users to get information about the treatises of the philosophers which I have read and for which I have made a synopsis. The API also provides RESTful endpoints for retrieving books, authors, and notes.

## Features

- User authentication using Flask-Login: The app supports user authentication to access the admin interface. Administrators can log in using their username, password, and a secret word.
- Database management using SQLAlchemy and Flask-Migrate: The app uses SQLAlchemy to interact with the database and Flask-Migrate for database migrations.
- Admin interface: The admin interface provides forms for adding books, authors, and notes. Administrators can enter the required information and submit the forms to store the data in the database.
- Error handling and flash messages: The app includes error handling to handle exceptions and display flash messages to provide feedback to the user.

## Routes
- / (Home page): Renders the home page.
- /admin (Admin login page): Handles the admin login route.
- /admin/interface (Admin interface): Provides an interface for managing books, authors, and notes.
- /logout (Logout route): Handles the logout route.
- /get/all_books (Retrieve all books or books by a specific author): Retrieves all books or books by a specific author.
- /get/authors (Retrieve authors): Retrieves all authors.
- /get/notes (Retrieve notes): Retrieves all notes or notes for a specific book.

## API Usage
The Philosophy API provides the following endpoints for retrieving data:

### Retrieve all books or books by a specific author
- Endpoint: /get/all_books
- Method: GET
- Parameters: author (optional): Filter books by author name
- Response:
    - If the author parameter is not provided:
        - Body: JSON object with an array of book objects
            - Each book object contains the following fields:
                - id: Book ID
                - title: Book title
             
    - If author parameter is provided:
        - If the author exists:
            - Body: JSON object with an array of book objects belonging to the specified author
                - Each book object contains the following fields:
                    - id: Book ID
                    - title: Book title
        - If the author does not exist:
            - Status code: 404 (Not Found)
            - Body: JSON object with an error message
### Retrieve authors
- Endpoint: /get/authors
- Method: GET
- Response:
    - Body: JSON object with an array of author objects
        - Each author object contains the following fields:
            - id: Author ID
            - name: Author name
            - biography: Author biography
         
### Retrieve notes
- Endpoint: /get/notes
- Method: GET
- Parameters: book (optional): Filter notes by book title
- Response:
    - If the book parameter is not provided:
        - Body: JSON object with an array of note objects
            - Each note object contains the following fields:
                - id: Note ID
                - book: Book title
                - content: Note content
                - chapter: Chapter name
    - If book parameter is provided:
        - If the book exists:
            - Body: JSON object with an array of note objects belonging to the specified book
                - Each note object contains the following fields:
                    - id: Note ID
                    - content: Note content
                    - chapter: Chapter name
        - If the book does not exist:
            - Status code: 404 (Not Found)
            - Body: JSON object with an error message
