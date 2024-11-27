## Secure File Sharing System
<hr>

### Backend Assessment for EZ Works
This project is a secure file-sharing system implemented as part of the backend engineer assessment for **EZ Works**. <br>

Once verified, login into your account and you will recieve a token. Add it to the `Authorization` header to make protected requests. <br>
You can now list files, generate download links and download the files. <br>

It provides a RESTful API for secure file upload, download, and management between two types of users: Operation Users and Client Users.
<hr>

### Features
#### Technology Stack
- **Framework**: Flask
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **File Type Detection**: python-magic

#### User Authentication:
- Secure signup and login for both user types
- Email verification for new users
- JWT-based authentication

#### Security Measures:
- Content-based file type verification
- Secure file storage
- Encrypted download URLs with expiration

#### File Management:
- Secure file upload (restricted to Operation Users)
- File listing
- Secure file download with encrypted URLs

#### User Roles:
- Operation User: Can upload, download files and list files
- Client User: Can download files and list files
<hr>

### API Endpoints
#### Authentication
- **POST** /signup: Sign up a new user
- **GET** /verify-email/<token>: Verify user's email
- **POST** /login: Log in a user

#### File Operations
- **POST** /upload: Upload a file (Operation Users only)
- **GET** /files: List all uploaded files
- **GET** /download/<file_id>: Generate a download link for a file
- **GET** /secure-download/<token>: Download a file using a secure token
<hr>


### Security Considerations
- File types are verified by content, not just extension
- Download URLs are encrypted and have a short expiration time
- User passwords are hashed before storage
<hr>


# secure_file_sharing_system_ezworks_assesment
