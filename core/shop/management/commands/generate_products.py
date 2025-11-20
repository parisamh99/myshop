from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from django.core.files import File
import random
import os

from shop.models import ProductModel, ProductCategoryModel, StatusProductType
from accounts.models import User  # adjust path if needed


class Command(BaseCommand):
    help = "Generate 10 fake products with realistic buyable item images from local files"

    # Folder where local images are stored (inside the commands folder)
    IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "images")  # create `images/` in commands

    def get_random_local_image(self):
        """Pick a random image file from the local IMAGE_FOLDER"""
        if not os.path.exists(self.IMAGE_FOLDER):
            self.stdout.write(self.style.ERROR(f"Image folder not found: {self.IMAGE_FOLDER}"))
            return None

        images = [f for f in os.listdir(self.IMAGE_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        if not images:
            self.stdout.write(self.style.ERROR("No image files found in the images folder!"))
            return None

        chosen_image = random.choice(images)
        image_path = os.path.join(self.IMAGE_FOLDER, chosen_image)

        return File(open(image_path, "rb"), name=chosen_image)

    def handle(self, *args, **kwargs):
        fake = Faker(locale="fa_IR")

        users = list(User.objects.all())
        categories = list(ProductCategoryModel.objects.all())
        statuses = [choice.value for choice in StatusProductType]

        if not users:
            self.stdout.write(self.style.ERROR("No users found!"))
            return

        if not categories:
            self.stdout.write(self.style.ERROR("No product categories found!"))
            return

        for _ in range(10):
            title = fake.sentence(nb_words=3)
            slug = slugify(title, allow_unicode=True)

            image_file = self.get_random_local_image()

            product = ProductModel.objects.create(
                user=random.choice(users),
                title=title,
                slug=slug,
                image=image_file,                 # ✔️ assign local image
                stock=random.randint(1, 100),
                price=random.randint(10, 2000),
                discount_percent=random.choice([0, 5, 10, 15, 20, 25]),
                status=random.choice(statuses),
                description=fake.text(max_nb_chars=250)
            )

            product.proudct_category.set(
                random.sample(categories, random.randint(1, 3))
            )

        self.stdout.write(self.style.SUCCESS("Successfully created 10 fake products with local images!"))
