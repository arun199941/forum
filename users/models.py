from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default.png', upload_to="profile_pics")
    about = models.TextField(default="", max_length=500)
    country = models.TextField(default="", max_length=100)
    phone =PhoneField(blank=True, help_text='Contact phone number')
    def __str__(self):
        return f' {self.user.username} Profile'
