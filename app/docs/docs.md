# Simple Messenger API Documentation

## Base URL: `http://localhost:5000/api`

### 1. User Registration

**Endpoint:** `POST /register`

**Request Body (JSON):**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response (Success):**

```json
{
  "status": "success",
  "user_id": "uuid"
}
```

**Error Codes:**

- `400`: Invalid data format
- `409`: Username already taken

### 2. Authentication

**Endpoint:** `POST /login`

**Request Body (JSON):**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response (Success):**

```json
{
  "token": "jwt_token",
  "expires_in": 3600
}
```

**Error Codes:**

- `401`: Invalid credentials

### 3. Send Message

**Endpoint:** `POST /messages`

**Headers:**

```
Authorization: Bearer <jwt_token