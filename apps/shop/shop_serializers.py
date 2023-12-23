from rest_framework import serializers

from .models import CategoryModel, CategoryImageModel, ItemModel, ItemImageModel, ShopContactsModel, Review


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField

    class Meta:
        model = CategoryImageModel
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    images = CategoryImageSerializer(many=True)

    class Meta:
        model = CategoryModel
        fields = ['id', 'id_name', 'name', 'description', 'images']


class ItemImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField

    class Meta:
        model = ItemImageModel
        fields = ['image']


class ItemSerializer(DynamicFieldsModelSerializer):
    images = CategoryImageSerializer(many=True)
    category__id_name = serializers.CharField(source='category.id_name')

    class Meta:
        model = ItemModel
        fields = '__all__'


class ShopContactsSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = ShopContactsModel
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "item_set", "email", "first_name", "last_name", "text", "state", "rate_by_stars", "date"]
