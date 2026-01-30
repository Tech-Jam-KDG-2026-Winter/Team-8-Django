from django.db import models
from django.contrib.auth.models import User

class MenuPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    recipe = models.TextField()
    image = models.ImageField(upload_to='menus/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

