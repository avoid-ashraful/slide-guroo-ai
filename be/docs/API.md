# SlideGuroo API Documentation

**Version**: 2.0.0
**Base URL**: `http://localhost:8000/api`
**Authentication**: JWT Bearer Token

---

## Table of Contents

1. [Authentication](#authentication)
2. [Slides](#slides)
3. [Topics](#topics)
4. [Chat](#chat)
5. [Diagrams](#diagrams)
6. [Dashboard](#dashboard)
7. [Error Handling](#error-handling)
8. [Models](#models)

---

## Authentication

All endpoints except authentication endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_token_here>
```

### Register User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_verified": false,
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request` - Email already registered or username taken
- `422 Unprocessable Entity` - Invalid input data

---

### Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Expiry:** 7 days

**Errors:**
- `401 Unauthorized` - Incorrect email or password

---

### Get Current User

**GET** `/auth/me`

Get authenticated user's information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_verified": true,
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z"
}
```

**Errors:**
- `401 Unauthorized` - Invalid or expired token

---

### Verify Email

**POST** `/auth/verify-email`

Verify user's email address with token.

**Request Body:**
```json
{
  "token": "verification_token_from_email"
}
```

**Response:** `200 OK`
```json
{
  "message": "Email verified successfully"
}
```

**Errors:**
- `400 Bad Request` - Invalid or expired verification token

---

### Resend Verification Email

**POST** `/auth/resend-verification`

Resend email verification link.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "Verification email sent"
}
```

**Errors:**
- `400 Bad Request` - User not found or already verified

---

### Forgot Password

**POST** `/auth/forgot-password`

Request password reset link via email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password reset link sent to your email"
}
```

**Note:** Always returns 200 even if email doesn't exist (security best practice)

---

### Reset Password

**POST** `/auth/reset-password`

Reset password using token from email.

**Request Body:**
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password reset successfully"
}
```

**Errors:**
- `400 Bad Request` - Invalid or expired reset token

---

## Slides

### Upload Slide

**POST** `/slides/upload`

Upload a presentation file (PPT, PPTX, PDF) and generate an AI lesson.

**Authentication:** Required (verified email)

**Request:** `multipart/form-data`

**Form Fields:**
- `file` (required): Presentation file (PPT/PPTX/PDF)
- `language` (optional): "en" or "bn" (default: "en")
- `difficulty_level` (optional): "beginner", "intermediate", or "advanced" (default: "intermediate")
- `include_diagrams` (optional): boolean (default: true)

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/slides/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@presentation.pptx" \
  -F "language=en" \
  -F "difficulty_level=intermediate" \
  -F "include_diagrams=true"
```

**Response:** `200 OK`
```json
{
  "message": "Lesson generated successfully",
  "lesson": {
    "id": "lesson-uuid",
    "title": "Introduction to Photosynthesis",
    "summary": "Learn about the process of photosynthesis...",
    "language": "en",
    "difficulty_level": "intermediate",
    "sections": [
      {
        "title": "What is Photosynthesis?",
        "content": "Photosynthesis is the process...",
        "key_points": ["Plants convert sunlight...", "..."],
        "examples": ["Green plants...", "..."],
        "diagrams": [
          {
            "title": "Photosynthesis Process",
            "mermaid_code": "graph TD\n  A[Sunlight] --> B[Chlorophyll]...",
            "description": "This diagram shows..."
          }
        ]
      }
    ],
    "key_concepts": ["Chlorophyll", "Carbon Dioxide", "Glucose"],
    "prerequisites": ["Basic biology"],
    "next_topics": ["Plant respiration", "Cell structure"]
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid file type or file too large
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Email not verified
- `422 Unprocessable Entity` - Invalid parameters

**Supported File Types:**
- PowerPoint: `.ppt`, `.pptx`
- PDF: `.pdf`

**File Size Limit:** 50 MB

---

## Topics

### Generate Topic Lesson

**POST** `/topics/generate`

Generate an AI lesson from a topic name.

**Authentication:** Required (verified email)

**Request Body:**
```json
{
  "topic": "Photosynthesis",
  "language": "en",
  "difficulty_level": "intermediate",
  "include_diagrams": true,
  "context": "Class 10 Biology"
}
```

**Parameters:**
- `topic` (required): Topic name or description
- `language` (optional): "en" or "bn" (default: "en")
- `difficulty_level` (optional): "beginner", "intermediate", or "advanced" (default: "intermediate")
- `include_diagrams` (optional): boolean (default: true)
- `context` (optional): Additional context for the lesson

**Response:** `200 OK`
```json
{
  "message": "Lesson generated successfully",
  "lesson": {
    "id": "lesson-uuid",
    "title": "Photosynthesis: The Food-Making Process",
    "summary": "Comprehensive guide to understanding photosynthesis...",
    "language": "en",
    "difficulty_level": "intermediate",
    "sections": [
      {
        "title": "Introduction to Photosynthesis",
        "content": "Detailed explanation...",
        "key_points": ["Point 1", "Point 2"],
        "examples": ["Example 1", "Example 2"],
        "diagrams": [...]
      }
    ],
    "key_concepts": ["Chlorophyll", "Light-dependent reactions"],
    "prerequisites": ["Basic cell biology"],
    "next_topics": ["Cellular respiration"]
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid topic or parameters
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Email not verified

---

## Chat

### Ask Question

**POST** `/chat/ask`

Ask a question about a lesson and get an AI response.

**Authentication:** Required (verified email)

**Request Body:**
```json
{
  "lesson_id": "lesson-uuid",
  "question": "What is the role of chlorophyll in photosynthesis?",
  "language": "en",
  "context": "I'm preparing for my exam",
  "conversation_history": []
}
```

**Parameters:**
- `lesson_id` (required): ID of the lesson to ask about
- `question` (required): User's question
- `language` (optional): "en" or "bn" (default: "en")
- `context` (optional): Additional context for the answer
- `conversation_history` (optional): Previous conversation (managed automatically)

**Response:** `200 OK`
```json
{
  "answer": "Chlorophyll is the green pigment found in plants that plays a crucial role in photosynthesis...",
  "related_concepts": ["Light absorption", "Photosystem I", "Photosystem II"],
  "additional_examples": [
    "Think of chlorophyll as solar panels for plants..."
  ],
  "follow_up_questions": [
    "How do different types of chlorophyll differ?",
    "What happens during the light-dependent reactions?"
  ]
}
```

**Errors:**
- `404 Not Found` - Lesson not found or access denied
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Email not verified

---

### Get Chat History

**GET** `/chat/history/{lesson_id}`

Retrieve all chat messages for a specific lesson.

**Authentication:** Required

**Parameters:**
- `lesson_id` (path): Lesson ID

**Response:** `200 OK`
```json
{
  "lesson_id": "lesson-uuid",
  "messages": [
    {
      "id": "message-uuid",
      "role": "user",
      "content": "What is photosynthesis?",
      "created_at": "2025-11-18T10:30:00Z"
    },
    {
      "id": "message-uuid-2",
      "role": "assistant",
      "content": "Photosynthesis is the process...",
      "related_concepts": ["Chlorophyll", "Sunlight"],
      "created_at": "2025-11-18T10:30:05Z"
    }
  ],
  "total": 2
}
```

**Errors:**
- `404 Not Found` - Lesson not found or access denied

---

### Delete Chat History

**DELETE** `/chat/history/{lesson_id}`

Delete all chat messages for a specific lesson.

**Authentication:** Required

**Parameters:**
- `lesson_id` (path): Lesson ID

**Response:** `200 OK`
```json
{
  "message": "Chat history deleted successfully",
  "deleted_count": 5
}
```

**Errors:**
- `404 Not Found` - Lesson not found or access denied

---

## Diagrams

### Generate Diagram

**POST** `/diagrams/generate`

Generate a Mermaid diagram for a specific concept.

**Authentication:** Required (verified email)

**Request Body:**
```json
{
  "concept": "Photosynthesis process",
  "diagram_type": "flowchart",
  "context": "Show the steps of photosynthesis"
}
```

**Parameters:**
- `concept` (required): Concept to visualize
- `diagram_type` (optional): "flowchart", "sequence", "class", "state", "entity-relationship"
- `context` (optional): Additional context for the diagram

**Response:** `200 OK`
```json
{
  "diagram": {
    "title": "Photosynthesis Process",
    "mermaid_code": "graph TD\n  A[Sunlight] --> B[Chlorophyll]\n  B --> C[Energy]\n  ...",
    "description": "This flowchart illustrates the step-by-step process of photosynthesis",
    "diagram_type": "flowchart"
  }
}
```

**Errors:**
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Email not verified

---

## Dashboard

### Get User Lessons

**GET** `/dashboard/lessons`

Get all lessons created by the authenticated user.

**Authentication:** Required

**Query Parameters:**
- `skip` (optional): Number of lessons to skip for pagination (default: 0)
- `limit` (optional): Maximum number of lessons to return (default: 20, max: 100)
- `source_type` (optional): Filter by source - "upload" or "topic"

**Example:**
```
GET /api/dashboard/lessons?skip=0&limit=10&source_type=upload
```

**Response:** `200 OK`
```json
{
  "lessons": [
    {
      "id": "lesson-uuid",
      "title": "Introduction to Photosynthesis",
      "source_type": "upload",
      "source_topic": null,
      "source_file": "presentation.pptx",
      "created_at": "2025-11-18T10:30:00Z",
      "updated_at": "2025-11-18T10:30:00Z",
      "total_sections": 5,
      "language": "en"
    }
  ],
  "total": 15,
  "skip": 0,
  "limit": 10
}
```

---

### Get Lesson Detail

**GET** `/dashboard/lessons/{lesson_id}`

Get detailed information about a specific lesson.

**Authentication:** Required

**Parameters:**
- `lesson_id` (path): Lesson ID

**Response:** `200 OK`
```json
{
  "id": "lesson-uuid",
  "title": "Introduction to Photosynthesis",
  "source_type": "upload",
  "source_topic": null,
  "source_file": "/uploads/user-id/file.pptx",
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z",
  "lesson": {
    "id": "lesson-uuid",
    "title": "Introduction to Photosynthesis",
    "summary": "...",
    "sections": [...],
    "key_concepts": [...],
    "prerequisites": [...],
    "next_topics": [...]
  }
}
```

**Errors:**
- `404 Not Found` - Lesson not found or access denied

---

### Delete Lesson

**DELETE** `/dashboard/lessons/{lesson_id}`

Delete a lesson and all associated chat history.

**Authentication:** Required

**Parameters:**
- `lesson_id` (path): Lesson ID

**Response:** `200 OK`
```json
{
  "message": "Lesson deleted successfully",
  "lesson_id": "lesson-uuid",
  "deleted_chat_messages": 10
}
```

**Errors:**
- `404 Not Found` - Lesson not found or access denied

---

### Get User Statistics

**GET** `/dashboard/stats`

Get statistics for the authenticated user.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "user": {
    "id": "user-uuid",
    "username": "johndoe",
    "email": "user@example.com",
    "is_verified": true,
    "joined_at": "2025-11-18T10:00:00Z"
  },
  "stats": {
    "total_lessons": 15,
    "lessons_from_upload": 8,
    "lessons_from_topic": 7,
    "total_chat_messages": 120,
    "total_questions_asked": 60
  },
  "recent_lesson": {
    "id": "lesson-uuid",
    "title": "Latest Lesson",
    "created_at": "2025-11-18T15:00:00Z"
  }
}
```

---

### Get Recent Activity

**GET** `/dashboard/recent-activity`

Get user's recent lessons and chat messages.

**Authentication:** Required

**Query Parameters:**
- `limit` (optional): Maximum number of items to return (default: 10, max: 50)

**Response:** `200 OK`
```json
{
  "recent_lessons": [
    {
      "id": "lesson-uuid",
      "title": "Photosynthesis",
      "source_type": "upload",
      "created_at": "2025-11-18T10:30:00Z"
    }
  ],
  "recent_chats": [
    {
      "id": "chat-uuid",
      "lesson_id": "lesson-uuid",
      "role": "user",
      "content": "What is photosynthesis?",
      "created_at": "2025-11-18T11:00:00Z"
    }
  ]
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required or token invalid |
| 403 | Forbidden | Authenticated but not authorized (e.g., email not verified) |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### Common Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden:**
```json
{
  "detail": "Email not verified"
}
```

**404 Not Found:**
```json
{
  "detail": "Lesson not found or you don't have access to it"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Models

### User

```typescript
{
  id: string;              // UUID
  email: string;           // Valid email address
  username: string;        // 3-20 characters, alphanumeric + underscore
  full_name: string;       // User's full name
  is_verified: boolean;    // Email verification status
  created_at: string;      // ISO 8601 timestamp
  updated_at: string;      // ISO 8601 timestamp
}
```

### Lesson

```typescript
{
  id: string;                    // UUID
  title: string;                 // Lesson title
  summary: string;               // Brief summary
  language: "en" | "bn";         // Language
  difficulty_level: string;      // "beginner" | "intermediate" | "advanced"
  sections: Section[];           // Lesson sections
  key_concepts: string[];        // Important concepts
  prerequisites: string[];       // Required knowledge
  next_topics: string[];         // Suggested next topics
}
```

### Section

```typescript
{
  title: string;              // Section title
  content: string;            // Main content
  key_points: string[];       // Important points
  examples: string[];         // Examples
  diagrams?: Diagram[];       // Optional diagrams
}
```

### Diagram

```typescript
{
  title: string;           // Diagram title
  mermaid_code: string;    // Mermaid.js code
  description: string;     // Diagram explanation
  diagram_type?: string;   // Optional type specification
}
```

### ChatMessage

```typescript
{
  id: string;                      // UUID
  lesson_id: string;               // Associated lesson
  role: "user" | "assistant";      // Message sender
  content: string;                 // Message content
  related_concepts?: string[];     // Related concepts (assistant only)
  created_at: string;              // ISO 8601 timestamp
}
```

---

## Rate Limiting

Currently, there are no rate limits enforced. For production deployment, consider implementing rate limiting based on your needs.

## Pagination

List endpoints support pagination using `skip` and `limit` query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum items to return (default varies by endpoint)

Example:
```
GET /api/dashboard/lessons?skip=20&limit=10
```
This fetches lessons 21-30.

---

## Development & Testing

### Base URLs

- **Development**: `http://localhost:8000/api`
- **Production**: Configure via `FRONTEND_URL` environment variable

### Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example Request (curl)

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get user info (replace TOKEN)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer TOKEN"

# Upload slide
curl -X POST http://localhost:8000/api/slides/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@presentation.pptx" \
  -F "language=en"
```

### Example Request (JavaScript/Fetch)

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { access_token } = await loginResponse.json();

// Get lessons
const lessonsResponse = await fetch('http://localhost:8000/api/dashboard/lessons', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});

const lessons = await lessonsResponse.json();
```

---

## Support

For issues or questions:
- **GitHub Issues**: https://github.com/avoid-ashraful/slide-guroo-ai/issues
- **Documentation**: See `be/docs/` directory

---

**Last Updated**: 2025-11-18
**API Version**: 2.0.0
