from django.conf import settings
from django.db import models

class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "男性"
        FEMALE = "F", "女性"
        OTHER = "O", "その他"
        NA = "N", "未回答"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    name = models.CharField("名前", max_length=50)
    age = models.PositiveSmallIntegerField("年齢", null=True, blank=True)
    weight_kg = models.DecimalField("体重(kg)", max_digits=5, decimal_places=1, null=True, blank=True)
    height_cm = models.DecimalField("身長(cm)", max_digits=5, decimal_places=1, null=True, blank=True)
    gender = models.CharField("性別", max_length=1, choices=Gender.choices, default=Gender.NA)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"