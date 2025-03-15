from django.core.management.base import BaseCommand
from users.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the database with 30 users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(30):
            phone_number = fake.phone_number()
            if len(phone_number) > 12:
                phone_number = phone_number[:20]
            User.objects.create_user(
                email=fake.email(),
                password='password123',
                name=fake.name(),
                company=fake.company(),
                phone_number=phone_number,
                country=fake.country(),
                status=fake.random_element(elements=('Active', 'Inactive'))
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with 30 users'))
