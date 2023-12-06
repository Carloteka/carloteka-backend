import os
import datetime
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.shop.models import CategoryModel, CategoryImageModel
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate entries for CategoryModel and CategoryImageModel.'

    def add_arguments(self, parser):
        parser.add_argument('num_entries', type=int, help='Number of entries to create')

    def handle(self, *args, **options):
        num_entries = options['num_entries']
        image_filename = 'img_data.png'
        image_path = os.path.join(settings.BASE_DIR, image_filename)

        for i in range(num_entries):
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            unique_id_name = f"ID_{timestamp}_{i}"

            category = CategoryModel.objects.create(id_name=unique_id_name, name="Имя категории",
                                                    description="Описание категории")

            with open(image_path, 'rb') as image_file:
                django_file = File(image_file)
                image_instance = CategoryImageModel(product_model=category)
                image_instance.image.save(f'image_{i}.png', django_file, save=True)

            self.stdout.write(self.style.SUCCESS(f'Image for category {category.id_name} created successfully'))

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_entries} entries'))
