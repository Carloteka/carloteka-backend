from django.contrib import admin

from .models import CategoryModel, CategoryImageModel


class ImageInline(admin.TabularInline):
    list_display = ['id_name', 'name', 'description']
    model = CategoryImageModel


class CategoryModelAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(CategoryModel, CategoryModelAdmin)
