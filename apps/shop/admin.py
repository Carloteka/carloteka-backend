from django.contrib import admin

from .models import (
    CategoryModel,
    CategoryImageModel,
    ItemModel,
    ItemImageModel,
    ShopContactsModel,
    OrderModel,
    ReviewModel,
    ItemStatsModel,
    OrderItemModel
)


class CategoryImageInline(admin.TabularInline):
    list_display = ['id_name', 'name', 'description']
    model = CategoryImageModel


class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInline]


class ItemImageInline(admin.TabularInline):
    list_display = '__all__'
    model = ItemImageModel


class ItemModelAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline]


admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(ItemModel, ItemModelAdmin)
admin.site.register(ShopContactsModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
admin.site.register(ReviewModel)
admin.site.register(ItemStatsModel)

