from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Generate users with unique email addresses'

    def handle(self, *args, **options):
        num_users = 15
        User = get_user_model()

        for i in range(num_users):
            base_username = f"user_{i}"
            base_email = f"user_{i}@example.com"
            password = "defaultpassword123"

            username = base_username
            email = base_email
            counter = 1
            while User.objects.filter(email=email).exists():
                username = f"{base_username}_{counter}"
                email = f"{base_username}_{counter}@example.com"
                counter += 1

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()

            self.stdout.write(self.style.SUCCESS(f'User successfully created {username} from email {email}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_users} users'))
