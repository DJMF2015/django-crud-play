from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Recipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    recipe_name = models.CharField(max_length=100, default='Recipe Name')
    recipe_description = models.TextField()
    recipe_ingredients = models.TextField(default=None)
    recipe_image = models.ImageField(upload_to='recipe_images', blank=True)
    recipe_view_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe_name
