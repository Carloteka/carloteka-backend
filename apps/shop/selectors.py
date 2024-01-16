from .models import CategoryModel


class CategorySelector():
    def category_list(self, params=None):
        queryset = CategoryModel.objects.all()
        return queryset
