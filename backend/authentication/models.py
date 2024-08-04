from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


# User model
class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    email_verified = models.BooleanField(default=False)
    games = models.ManyToManyField('core.Game', related_name='users', through='core.UserGame')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='default.jpg', default='user_images')

    def __str__(self):
        return self.user.username


# Signal to create a profile when a user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Signal to save the profile when a user is saved
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Connect the signals
post_save.connect(create_user_profile, sender=User)





