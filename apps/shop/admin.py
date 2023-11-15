from django.contrib import admin

from .models import CategoryModel, CategoryImageModel, ItemModel, ItemImageModel


class CategoryImageInline(admin.TabularInline):
    list_display = ['id_name', 'name', 'description']
    model = CategoryImageModel


class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInline]


admin.site.register(CategoryModel, CategoryModelAdmin)


class ItemImageInline(admin.TabularInline):
    list_display = '__all__'
    model = ItemImageModel


class ItemModelAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline]


admin.site.register(ItemModel, ItemModelAdmin)
