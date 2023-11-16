# Categories

Get categories

**URL** : `/shop/categories/`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
[
  {
      "id": 1,
      "id_name": "shakhy-shashky-nardy",
      "name": "ШАХИ, НАРДИ, ШАШКИ",
      "description": "Тут ви знайдете зброю з ...",
      "images": [
        {
          "image": "/media/images/photo_1_m3iAxLe.png"
        },
        {
          "image": "/media/photos/product/images/photo_2.png"
        }
    ],
  },
  {
      "id": 1,
      "id_name": "dereviana-zbroya",
      "name": "ДЕРЕВ'ЯНА ЗБРОЯ: МЕЧІ, ШАБЛІ, КАТАНИ, ЩИТИ, НАБОРИ",
      "description": "Тут ви знайдете зброю з твердих порід дерева", 
      "images": [
        {
          "image": "/media/images/photo_1_m3iAxLeW.png"
        }
    ],
  }
]
```

## Error Responses

**Code** : `400`
