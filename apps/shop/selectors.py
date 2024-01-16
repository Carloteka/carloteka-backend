from .models import (
    CategoryModel,
    ShopContactsModel
)


class CategorySelector:
    def category_list(self, params=None):
        queryset = CategoryModel.objects.all()
        return queryset


class ShopContactsSelector:
    def shop_contacts_retrieve_no_pk(self):
        queryset = ShopContactsModel.objects.first()
        return queryset
