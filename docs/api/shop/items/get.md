# Items

## get items

**URL** : `/shop/items/`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

**Query Parameters**

```page_size=<int>``` - how many items you get

```page=<int>``` - what page of database (based on page_size) you taking items from

```price_from=<int>```

```price_to=<int>```

```in_stock=True```

```out_of_stock=True```

```backorder=True```

```specific_order=True```

```category_id_name=<category_id_name>``` - can be used more than one time

## Success Responses

**Code** : `200 OK`


```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/shop/items/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "images": [
        {
          "image": "http://127.0.0.1:8000/images/image_1_3127.png"
        },
        {
          "image": "http://127.0.0.1:8000/images/image_1_7666.png"
        }
      ],
      "category__id_name": "ID_20231212235019155732_0",
      "id_name": "Ваза декоративна_20231212235019209343_0",
      "name": "Ваза",
      "price": 50.0,
      "length": 1.5,
      "height": 2.0,
      "width": 0.5,
      "in_stock": 0,
      "mini_description": "Ваза",
      "mini_image": "http://127.0.0.1:8000/images/images/mini_image_0.png"
    },
    {
      "id": 2,
      "images": [
        {
          "image": "http://127.0.0.1:8000/images/image_2_5562.png"
        },
        {
          "image": "http://127.0.0.1:8000/images/image_2_6356.png"
        }
      ],
      "category__id_name": "ID_20231212235019155732_0",
      "id_name": "Ваза декоративна_20231212235019670911_1",
      "name": "Ваза",
      "price": 50.0,
      "length": 1.5,
      "height": 2.0,
      "width": 0.5,
      "in_stock": 3,
      "mini_description": "Ваза",
      "mini_image": "http://127.0.0.1:8000/images/images/mini_image_1.png"
    }
  ]
}
```

## Error Responses

**Code** : `400`