from django.contrib import admin

from .models import CategoryModel, CategoryImageModel, ItemModel, ItemImageModel, ShopContactsModel, OrderModel, ReviewModel


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
admin.site.register(ReviewModel)


# TODO why we need this?
# @admin.register(ReviewModel)
# class ReviewModelAdmin(admin.ModelAdmin):
#     list_display = ["id", "email", "first_name", "last_name", "text", "rate_by_stars", "state", "date", "updated_at"]
#     model = ReviewModel


