from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.deconstruct import deconstructible
import os


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', 'Dueño de Mascotas'),
        ('sitter', 'Cuidador de Mascotas'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.get_full_name() or self.username


class PetOwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name if full_name.strip() else self.user.username


class PetSitterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    experience_years = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    photo = models.ImageField(
        upload_to='sitter_photos/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name if full_name.strip() else self.user.username


# class Avatar(models.Model):
    # imagen = models.ImageField(upload_to="avatars/")
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"Avatar for {self.user.username}"


class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatars/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"Avatar for {self.user.username}"

    def save(self, *args, **kwargs):
        # Delete old avatar file if it exists
        old_avatar = Avatar.objects.filter(user=self.user).first()
        if old_avatar and old_avatar.pk != self.pk:
            if old_avatar.imagen and default_storage.exists(old_avatar.imagen.name):
                default_storage.delete(old_avatar.imagen.name)
            old_avatar.delete()

        # Set custom file name
        ext = os.path.splitext(self.imagen.name)[1]
        self.imagen.name = f"avatars/avatar_{self.user.id}{ext}"
        super().save(*args, **kwargs)
