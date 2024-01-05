# Django Notes API

This Django project provides a simple RESTful API for a note-taking application. It allows users to create, read, update, delete, and share notes. The project uses Django REST Framework for handling RESTful services.

## Features

- User authentication (signup and login)
- CRUD operations for notes
- Sharing notes with other users

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone [your-repository-url]
   cd [repository-name]

2. **Configure the settings:**
   ```settings.py
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '',
      }
    }

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

4. **Start the server:**
   ```bash
   python manage.py runserver

## API Endpoints

### User Authentication

1. **Signup**
   - **Method:** POST
   - **Endpoint:** `/auth/signup`
   - **Payload:** 
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```

2. **Login**
   - **Method:** POST
   - **Endpoint:** `/auth/login`
   - **Payload:** 
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```

### Notes Management

1. **Create Note**
   - **Method:** POST
   - **Endpoint:** `/notes/`
   - **Header:** `Authorization: Token <user_token>`
   - **Payload:** 
     ```json
     {
       "title": "string",
       "content": "string"
     }
     ```

2. **List Notes**
   - **Method:** GET
   - **Endpoint:** `/notes/`
   - **Header:** `Authorization: Token <user_token>`

3. **Get Note Detail**
   - **Method:** GET
   - **Endpoint:** `/notes/<note_id>/`
   - **Header:** `Authorization: Token <user_token>`

4. **Update Note**
   - **Method:** PUT
   - **Endpoint:** `/notes/<note_id>/`
   - **Header:** `Authorization: Token <user_token>`
   - **Payload:** 
     ```json
     {
       "title": "string",
       "content": "string"
     }
     ```

5. **Delete Note**
   - **Method:** DELETE
   - **Endpoint:** `/notes/<note_id>/`
   - **Header:** `Authorization: Token <user_token>`

### Sharing Notes

1. **Share Note**
   - **Method:** POST
   - **Endpoint:** `/notes/<note_id>/share/`
   - **Header:** `Authorization: Token <user_token>`
   - **Payload:** 
     ```json
     {
       "username": "string"
     }
     ```
