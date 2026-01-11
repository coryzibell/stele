# API Integration Guide

Complete guide for integrating with our platform API.

## Authentication

All API requests require authentication. We support two methods:

1. OAuth 2.0 (recommended for web applications)
2. API Keys (recommended for server-to-server)

### Getting Started with OAuth

Register your application in the developer portal to obtain client credentials:

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "redirect_uri": "https://yourapp.com/callback"
}
```

### API Key Authentication

Generate an API key from your account settings. Include it in all requests:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/users
```

## Endpoints

### User Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| /v1/users | GET | List all users |
| /v1/users/:id | GET | Get user details |
| /v1/users | POST | Create new user |
| /v1/users/:id | PUT | Update user |
| /v1/users/:id | DELETE | Delete user |

### Data Operations

Common operations for managing data:

- **Create**: POST new records to the collection
- **Read**: GET records with optional filters
- **Update**: PUT or PATCH existing records
- **Delete**: DELETE records by ID

Example request:

```python
import requests

url = "https://api.example.com/v1/data"
headers = {"Authorization": "Bearer YOUR_API_KEY"}
data = {
    "name": "Sample Dataset",
    "values": [1, 2, 3, 4, 5]
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Rate Limiting

Rate limits vary by plan:

| Plan | Requests/Hour | Burst Limit |
|------|---------------|-------------|
| Free | 100 | 10 |
| Starter | 1,000 | 50 |
| Pro | 10,000 | 200 |
| Enterprise | Unlimited | Unlimited |

When you exceed the rate limit, you'll receive a 429 status code:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Try again in 3600 seconds.",
  "retry_after": 3600
}
```

## Error Handling

The API uses standard HTTP status codes:

- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Rate Limit Exceeded
- **500**: Internal Server Error

Example error response:

```json
{
  "error": "invalid_request",
  "message": "Missing required field: email",
  "field": "email",
  "code": "MISSING_FIELD"
}
```

## Webhooks

Configure webhooks to receive real-time notifications:

1. Register webhook URL in dashboard
2. Select event types to monitor
3. Verify webhook signature
4. Process incoming payloads

Example webhook payload:

```json
{
  "event": "user.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "user_id": "usr_123456",
    "email": "newuser@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

## Best Practices

Follow these guidelines for reliable integration:

- Cache responses when possible
- Implement exponential backoff for retries
- Use compression for large payloads
- Monitor your rate limit usage
- Handle errors gracefully
- Keep API keys secure

### Code Example

Complete integration example:

```javascript
const axios = require('axios');

class APIClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.example.com/v1';
  }

  async getUsers() {
    try {
      const response = await axios.get(`${this.baseURL}/users`, {
        headers: { 'Authorization': `Bearer ${this.apiKey}` }
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error.message);
      throw error;
    }
  }
}

// Usage
const client = new APIClient('your_api_key');
client.getUsers().then(users => console.log(users));
```
