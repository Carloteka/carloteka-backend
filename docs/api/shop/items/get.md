# Items

## get items

**URL** : `/shop/items/`

**Method** : `GET`

**Auth required** : NO 

**Permissions required** : NONE

**Query Parameters**

```page-size=<int>``` - how many items you get

```page=<int>``` - what page of database (based on page_size) you taking items from

```price-from=<int>```

```price-to=<int>```

```in-stock=True```

```out-of-stock=True```

```backorder=True```

```specific-order=True```

```category-id-name=<category_id_name>``` - can be used more than one time

```"sort-by"=price-up``` - sort by ascending price

```"sort-by"=price-down``` - sort by descending price


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
          "image": "/images/image_1_3127.png"
        },
        {
          "image": "/images/image_1_7666.png"
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
      "mini_image": "/images/images/mini_image_0.png"
    },
    {
      "id": 2,
      "images": [
        {
          "image": "/images/image_2_5562.png"
        },
        {
          "image": "/images/image_2_6356.png"
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
      "mini_image": "/images/images/mini_image_1.png"
    }
  ]
}
```

## Error Responses

**Code** : `400`