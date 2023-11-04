# Item 

get items details

**URL** : `/shop/categories/<str:id_name>/items/<int:id_name>`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

## Success Responses

**Code** : `200 OK`


```json
{
    "id": 1,
    "id_name": "vakidzashi-63",
    "name": "Вакідзаші: коротки меч самурая",
    "price": 550,
    "discounted_price": null,
    "length": 60,
    "height": null,
    "width": null,
    "in_stock": 1,
    "mini_description": "Вакідзаші: коротки меч самурая",
    "description": "Ми постаралися зробити копію японського меча Вакідзасі з дерева...",
    "mini_image": "/media/photos/product/mini_image/photo_1_4MB4slz.png",
    "visits": 0,
    "category__id_name": "dereviana-zbroya",
    "images": [
      {
        "image": "/media/photos/product/images/photo_1_m3iAxLe.png"
      },
      {
        "image": "/media/photos/product/images/photo_2.png"
      },
      {
        "image": "/media/photos/product/images/photo_3.png"
      },
      {
        "image": "/media/photos/product/images/photo_6.png"
      }
    ]
}
```

## Error Responses

**Code** : `400`
