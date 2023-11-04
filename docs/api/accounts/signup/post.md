# Sign up

Create a user account

**URL** : `/accounts/signup/`

**Method** : `POST`

**Auth required** : NO 

**Permissions required** : NONE

**Data to send**

```json
{
    "email": "savytskyi.work@gmail.com", 
    "password": "abc123456",
    "repeat_password": "abc123456",
  
    // optional
    "name": "Anton",
    "surname": "Savytskyi"
}
```

## Success Responses

**Code** : `201 CREATED`


```json
{
    "id": 2,
    "email": "savytskyi.work@gmail.com"
}
```

## Error Responses

**Code** : `400`
