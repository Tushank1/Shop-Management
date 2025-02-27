# Shop Management API Documentation

## **Project Overview**
The **Shop Management API** is a FastAPI-based backend system that allows **vendors** to perform CRUD operations on their shops and provides a **public API** for users to search for nearby shops.

### **Features**
- **Vendor Authentication** (JWT-based login & registration)
- **Shop Management** (Create, Read, Update, Delete)
- **Nearby Shop Search API** (Public access, based on latitude & longitude)
- **Secure Role-based Access** (Only authenticated vendors can manage shops)
- **Unit Testing** (Ensure API reliability)

---
## **1. Project Setup**

### **1.1 Prerequisites**
- Python 3.8+
- PostgreSQL (or SQLite for local development)
- FastAPI, SQLAlchemy, and other dependencies

### **1.2 Install Dependencies**
```bash
pip install -r requirements.txt
```

### **1.3 Set Up Environment Variables**
Create a `.env` file in the root directory with:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **1.4 Start the FastAPI Server**
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

---
## **2. API Endpoints**

### **2.1 Vendor Authentication**
#### **Register Vendor**
```http
POST /vendors/register
```
**Request Body:**
```json
{
    "name": "Vendor Name",
    "email": "vendor@example.com",
    "password": "securepassword"
}
```

#### **Login Vendor (Get JWT Token)**
```http
GET /vendors/token?email=vendor@example.com&password=securepassword
```
**Response:**
```json
{
    "access_token": "jwt_token_here"
}
```

---
### **2.2 Shop Management (Requires Authentication)**

#### **Create a Shop**
```http
POST /shops/create
```
**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "name": "Shop Name",
    "type": "Grocery",
    "latitude": 40.712776,
    "longitude": -74.005974
}
```

#### **Retrieve All Shops (For Authenticated Vendor)**
```http
GET /shops/retrieve
```

#### **Update Shop Details**
```http
PUT /shops/update/{shop_id}
```
**Request Body:** (Only include fields to update)
```json
{
    "name": "Updated Shop Name",
    "latitude": 41.12345
}
```

#### **Delete a Shop**
```http
DELETE /shops/delete/{shop_id}
```

---
### **2.3 Public API for Nearby Shops**
#### **Search Nearby Shops (No Authentication Required)**
```http
GET /search/nearby_shops?latitude=40.7128&longitude=-74.0060&radius=5
```
**Response:**
```json
[
    {
        "name": "Shop A",
        "type": "Electronics",
        "latitude": 40.712776,
        "longitude": -74.005974
    }
]
```

---
## **3. Running Tests**
Run unit tests using **pytest**:
```bash
pytest test_main.py --disable-warnings
```

---
## **4. Security Considerations**
- **Passwords are hashed using bcrypt** before storage.
- **JWT authentication** is enforced for shop management.
- **Role-based access control** ensures only vendors manage their shops.
- **Rate limiting & input validation** prevents API abuse.

---
## **5. Contribution Guide**
### **5.1 Fork & Clone Repository**
```bash
git clone https://github.com/Tushank1/Shop-Management.git
```
### **5.2 Create a New Branch**
```bash
git checkout -b feature-new-feature
```
### **5.3 Commit & Push Changes**
```bash
git commit -m "Added new feature"
git push origin feature-new-feature
```
