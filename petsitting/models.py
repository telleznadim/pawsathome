from django.db import models
from accounts.models import PetOwnerProfile, PetSitterProfile


class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(PetOwnerProfile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='pet_photos/',
                              blank=True, null=True)  # ← Add this line

    def __str__(self):
        return f"{self.name} ({self.species})"


class JobRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    owner = models.ForeignKey(
        PetOwnerProfile, on_delete=models.CASCADE, related_name='job_requests')
    sitter = models.ForeignKey(
        PetSitterProfile, on_delete=models.CASCADE, related_name='job_requests')
    pets = models.ManyToManyField(Pet)
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job for {self.owner.user.username} with {self.sitter.user.username} ({self.status})"
