## 🧰 Setup Instructions

### 1. Clone the Project

git clone https://github.com/yourusername/gutenberg-api.git
cd gutenberg-api

### 2. Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate # Windows

### 3. Install Dependencies

pip install fastapi uvicorn sqlalchemy pymysql

### 4. Import MySQL Dump

CREATE DATABASE gutenberg;
USE gutenberg;
\. C:/path/to/gutendex.sql

### 5. Run the API

Run:
uvicorn main:app --reload

Visit :
http://127.0.0.1:8000/docs


