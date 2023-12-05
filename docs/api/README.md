# CARLOTEKA api documentation 

Documentation of carloteka api

### Accounts related

[//]: # ()
[//]: # (Auth)

[//]: # ()
[//]: # (* [Sign up]&#40;accounts/signup/post.md&#41; : `POST /accounts/signup/`)

* [Log in](accounts/login/post.md) : `POST /accounts/login/`

[//]: # (* [Sign up or Login via google]&#40;accounts/google/login/post.md&#41; : `POST /accounts/google/login/` &#40;no docs&#41;)

[//]: # (* [Sign up or Login via Facebook]&#40;accounts/facebook/login/post.md&#41; : `POST /accounts/facebook/login/` &#40;no docs&#41;)

* [Refresh token](accounts/token/refresh/post.md) : `POST /accounts/token/refresh/`

[//]: # (* [Get user]&#40;accounts/users/pk/get.md&#41; : `GET /accounts/users/<int:pk>`)

[//]: # (* [Update user]&#40;accounts/users/pk/patch.md&#41; : `PATCH /accounts/user/<int:pk>`)

[//]: # (* [Delete user]&#40;accounts/users/pk/delete.md&#41; : `DELETE /accounts/user/<int:pk>`)


[//]: # (* [Create user address]&#40;accounts/users/pk/adress/post.md&#41; : `POST /accounts/user/<int:pk>/adress`)

[//]: # (* [Get user address]&#40;accounts/users/pk/adress/get.md&#41; : `GET /accounts/user/<int:pk>/adress`)

[//]: # (* [Update user address]&#40;accounts/users/pk/adress/put.md&#41; : `PUT /accounts/user/<int:pk>/adress`)

[//]: # (* [delete user address]&#40;accounts/users/pk/adress/delete.md&#41; : `DELETE /accounts/user/<int:pk>/adress`)


### Shop related

#### Endpoints for all shop logic on the website

Categories

* [Get categories](shop/categories/get.md) : `GET /shop/categories/`

Items

* [Get items](shop/items/get.md) : `GET /shop/items/`
* [Get item](shop/items/pk/get.md) : `GET /shop/items/<int:pk>/`
* [Get item](shop/categories/id_name/items/id_name/get.md) : `GET /shop/categories/<str:category_id_name>/items/<int:item_id_name>/`
* [Update items](shop/items/pk/patch.md) : `PATCH /shop/items/<int:pk>/`

Website contacts

* [Get shop contacts](shop/contacts/get.md) : `GET /shop/contacts/`
 
Orders

[//]: # ()
[//]: # (* [Get orders]&#40;shop/orders/get.md&#41; : `GET /shop/orders` &#40;dev&#41;)

* [Get order](shop/orders/pk/get.md) : `GET /shop/orders/<int:pk>/` (dev)

[//]: # (* [Create order]&#40;shop/orders/post.md&#41; : `POST /shop/orders` &#40;dev&#41;)

[//]: # (* [Update order]&#40;shop/orders/pk/patch.md&#41; : `PATCH /shop/orders/<int:pk>` &#40;dev&#41;)

[//]: # ()
Reviews

[//]: # ()
[//]: # (* [Get items' reviews]&#40;shop/items/pk/reviews/get.md&#41; : `GET /shop/itmes/<int:pk>/reviews` &#40;dev&#41;)

[//]: # (* [Create review]&#40;shop/reviews/post.md&#41; : `POST /shop/reviews` &#40;dev&#41;)


### Nova Posta 


### Payment Provider
