# CARLOTEKA api documentation 

Documentation of carloteka api

### Accounts related

Auth

* [Sign up]() : `POST /accounts/signup/`
* [Log in]() : `POST /accounts/login/`
* [Sign up or Login via google](accounts/google/login/post.md) : `POST /accounts/google/login/`
* [Sign up or Login via Facebook](accounts/facebook/login/post.md) : `POST /accounts/facebook/login/`
* [Update password]() : `POST /accounts/user/`


* [Refresh token](accounts/token/refresh/post.md) : `POST /accounts/token/refresh/`


Users


* [Get user]() : `GET /accounts/users/<int:pk>`
* [Update user]() : `PATCH /accounts/user/<int:pk>`
* [Delete user]() : `DELETE /accounts/user/<int:pk>`


* [Create user address]() : `POST /accounts/user/<int:pk>/adress`
* [Get user address]() : `GET /accounts/user/<int:pk>/adress`
* [Update user address]() : `PUT /accounts/user/<int:pk>/adress`
* [delete user address]() : `DELETE /accounts/user/<int:pk>/adress`


### Shop related

Endpoints for all shop logic on the website

* [Get categories]() : `GET /shop/categories`

Items

* [Get items]() : `GET /shop/items`
* [Get item]() : `GET /shop/items/<int:pk>`
* [Update items]() : `PATCH /shop/items/<int:pk>`

Filters

* [Get filters]() : `GET /shop/filters`

Website contacts

* [Get shop contacts]() : `GET /shop/contacts`
 
Orders

* [Get orders]() : `GET /shop/orders`
* [Get order]() : `GET /shop/orders/<int:pk>`
* [Create order]() : `POST /shop/orders`
* [Update order]() : `PATCH /shop/orders`


### Nova Posta 


### Payment Provider
