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
    "id_name": "vakidzashi-63", 
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
    ],
    "name": "Вакідзаші: коротки меч самурая",
    "price": 550,
    "discounted_price": null,
    "length": 60,
    "height": null,
    "width": null,
    "in_stock": 1,
    "mini_description": "Вакідзаші: коротки меч самурая",
    "description": "Ми постаралися зробити копію японського меча Вакідзасі з дерева. У цій позиції є деякі зміни, на відміну від попередніх мечів. Ми подовжили рукоятку з 15 до 18 см, змінили форму леза і зробили нову фігурну цубу, так, щоб меч максимально був схожим на справжній. У підсумку ми отримали елегантний та красивий японський меч Вакідзасі, який буде чудовим подарунком!  Вироби виготовлені в Україні з екологічно чистого матеріалу, натурального дерева твердих порід акації або шовковиці. Лак та фарба не використовується.  Вироби добре відшліфовані, не мають зазубрин і сколів. Особливістю цих мечів є те, що лезо та рукоять зроблені з єдиного, цільного масиву дерева, що робить їх особливо міцними, збільшує термін служби виробу і дає можливість використовувати ці мечі як тренувальну зброю.  Хорошим подарунком може стати набір мечів чи японські мечі на дерев'яній підставці.",
    "mini_image": "/media/photos/product/mini_image/photo_1_4MB4slz.png",
    "visits": 0,
    "category": 1
  },
  {
    // similar item
  }
]
```

## Error Responses

**Code** : `400`