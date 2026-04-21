from django.db import models


class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = 'TREE', 'Tree'
        FRUIT = 'FRUIT', 'Fruit'
        VEGETABLE = 'VEGETABLE', 'Vegetable'
        FLOWER = 'FLOWER', 'Flower'
        HERB = 'HERB', 'Herb'

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    # NOTE: pip install Pillow is required for ImageField support
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
