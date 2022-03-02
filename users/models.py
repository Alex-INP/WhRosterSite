from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class NormalUser(AbstractUser):
	first_name = models.CharField('first name', max_length=150)
	last_name = models.CharField('last name', max_length=150)
	email = models.EmailField('email address', unique=True)


class UserProfile(models.Model):
	rosters_count = models.PositiveIntegerField("total roser count", default=0)
	user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, db_index=True)

	def __str__(self):
		return f"{self.user} profile"

	@receiver(post_save, sender=NormalUser)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(user=instance)
