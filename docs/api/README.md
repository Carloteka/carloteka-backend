# CARLOTEKA api documentation 

Documentation of carloteka api

### Accounts related

[//]: # ()
[//]: # (Auth)

[//]: # ()
[//]: # (* [Sign up]&#40;accounts/signup/post.md&#41; : `POST /accounts/signup/`)

[//]: # (* [Log in]&#40;accounts/login/post.md&#41; : `POST /accounts/login/`)

[//]: # (* [Sign up or Login via google]&#40;accounts/google/login/post.md&#41; : `POST /accounts/google/login/` &#40;no docs&#41;)

[//]: # (* [Sign up or Login via Facebook]&#40;accounts/facebook/login/post.md&#41; : `POST /accounts/facebook/login/` &#40;no docs&#41;)

[//]: # ()
[//]: # ()
[//]: # (* [Refresh token]&#40;accounts/token/refresh/post.md&#41; : `POST /accounts/token/refresh/` )

[//]: # ()
[//]: # ()
[//]: # (Users)

[//]: # ()
[//]: # ()
[//]: # (* [Get user]&#40;accounts/users/pk/get.md&#41; : `GET /accounts/users/<int:pk>`)

[//]: # (* [Update user]&#40;accounts/users/pk/patch.md&#41; : `PATCH /accounts/user/<int:pk>`)

[//]: # (* [Delete user]&#40;accounts/users/pk/delete.md&#41; : `DELETE /accounts/user/<int:pk>`)

[//]: # ()
[//]: # ()
[//]: # (* [Create user address]&#40;accounts/users/pk/adress/post.md&#41; : `POST /accounts/user/<int:pk>/adress`)

[//]: # (* [Get user address]&#40;accounts/users/pk/adress/get.md&#41; : `GET /accounts/user/<int:pk>/adress`)

[//]: # (* [Update user address]&#40;accounts/users/pk/adress/put.md&#41; : `PUT /accounts/user/<int:pk>/adress`)

[//]: # (* [delete user address]&#40;accounts/users/pk/adress/delete.md&#41; : `DELETE /accounts/user/<int:pk>/adress`)


### Shop related

Endpoints for all shop logic on the website

* [Get categories](shop/categories/get.md) : `GET /shop/categories`

Items

* [Get items](shop/items/get.md) : `GET /shop/items`
* [Get item](shop/categories/id_name/items/id_name/get.md) : `GET /shop/categories/<str:id_name>/items/<int:id_name>`
* [Update items](shop/items/pk/patch.md) : `PATCH /shop/items/<int:pk>`

Website contacts

* [Get shop contacts](shop/contacts/get.md) : `GET /shop/contacts`
 
Orders

* [Get orders](shop/orders/get.md) : `GET /shop/orders`
* [Get order](shop/orders/pk/get.md) : `GET /shop/orders/<int:pk>`
* [Create order](shop/orders/post.md) : `POST /shop/orders`
* [Update order](shop/orders/pk/patch.md) : `PATCH /shop/orders/<int:pk>`


### Nova Posta 


### Payment Provider
