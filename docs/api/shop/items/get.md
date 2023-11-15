# Items

get items

**URL** : `/shop/items/`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
[
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
        "length": null,
        "height": null,
        "width": null,
        "mini_description": "Бокс для шахів",
        "mini_image": "/images/Screenshot_from_2023-11-14_15-24-48_Z0wHI3f.png"
    },
    {
        "id": 2,
        "images": [
            {
                "image": "/images/Screenshot_from_2023-11-14_15-24-48.png"
            },
            {
                "image": "/images/Screenshot_from_2023-11-14_15-26-33_H4Odwd6.png"
            }
        ],
        "category__id_name": "shakhy-shashky-nardy",
        "id_name": "chess-box1",
        "name": "Бокс для шахів",
        "price": 1990.0,
        "length": null,
        "height": null,
        "width": null,
        "mini_description": "Бокс для шахів",
        "mini_image": "/images/Screenshot_from_2023-11-14_15-24-48_Z0wHI3f.png"
    }
]
```

## Error Responses

**Code** : `400`