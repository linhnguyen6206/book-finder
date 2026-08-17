# **Book Finder**
A full-stack web application that allows users to create an account, search for books, and save their favorites. This project uses Google Books API.

## **Features**
* Create an account/Sign in to keep a record of books
* Search for books and save favorites

## **Technologies Used**
* Google Books API

## **Getting Started**
### **Prerequisites**
* Obtain Google Books API from Google Cloud.

### **Installation**
1. Clone the repository
```
git clone https://github.com/linhnguyen6206/book-finder/
cd book-finder
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Add API key to .env
```
cd backend
vim .env
```
* Add API key to GOOGLE_BOOKS_API
* Add JWT_SECRET_KEY:
```
python3 -c "import secrets; print(secrets.token_hex(32))"
```
5. Run backend
```
cd backend
uvicorn main:app --reload
```
### **Running the Application**
1. Open book-finder.html. The app will be hosted on https://localhost:8000 on your browser to view the application. 
