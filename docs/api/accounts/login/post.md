# Login

Login user

**URL** : `/accounts/login/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : NONE

**Data to send**

```json
{
    "email": "savytskyi.work@gmail.com", 
    "password": "abc123456",
}
```

## Success Responses

**Code** : `200 OK`


```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk5Mjk1MjEwLCJpYXQiOjE2OTkxMjI0MTAsImp0aSI6IjAzOTRmZDhkY2QyMzQ5ZTJiZjI4MDdjY2E4NTYyYmQ2IiwidXNlcl9pZCI6NH0.6W1bLFuSP69NozbggZyUoIC7Q6SOEi409FGLYmr_-yI",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTcxNDQxMCwiaWF0IjoxNjk5MTIyNDEwLCJqdGkiOiI2YTMxYmU4ZjZlOTA0MDY1OWI5OTgzNzk0ZDdiYTI0ZCIsInVzZXJfaWQiOjR9.JavVoq-neQXDjJY7JB5bNLV3bKv1ISkJ7PAjJQRID7g",
    "user": {
        "pk": 2,
        "email": "savytskyi.work@gmail.com"
    }
}
```

## Error Responses

**Code** : `400`
