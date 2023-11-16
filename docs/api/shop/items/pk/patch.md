# Categories

Get categories

**URL** : `/shop//items/<int:pk>`

**Method** : `PATCH`

**Auth required** : YES

**Permissions required** : STAFF

## Success Responses

**Code** : `200 OK`

one or more of follow fields
```json
{
    "id": 1,
    "category__id_name": "shakhy-shashky-nardy",
    "id_name": "chess-box",
    "name": "Бокс для шахів",
    "price": 1990.0,
    "discounted_price": null,
    "length": null,
    "height": null,
    "width": null,
    "in_stock": 1,
    "mini_description": "Бокс для шахів",
    "description": "...",
    "category": 1
}
```

## Error Responses

**Code** : `400`
