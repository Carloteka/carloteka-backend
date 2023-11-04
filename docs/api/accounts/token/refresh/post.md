# Refresh Token

Get access token with refresh token

**URL** : `/accounts/token/refresh/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : NONE

**Data to send**

```json
{
    "refresh": "token"
}
```

## Success Responses

**Code** : `200 OK`

```json
{
    "access": "token"
}
```

## Error Responses

**Code** : `400`
