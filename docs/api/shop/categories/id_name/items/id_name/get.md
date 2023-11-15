# Item 

get items details

**URL** : `/shop/categories/<str:category_id_name>/<int:item_id_name>`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
{
    "id": 1,
    "images": [
        {
            "image": "/images/Screenshot_from_2023-11-14_15-24-48.png"
        },
        {
            "image": "/images/Screenshot_from_2023-11-14_15-26-33_H4Odwd6.png"
        }
    ],
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
    "description": "Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів, Бокс для шахів",
    "visits": 0,
    "mini_image": "/images/Screenshot_from_2023-11-14_15-24-48_Z0wHI3f.png",
    "category": 1
}
```

## Error Responses

**Code** : `400`
