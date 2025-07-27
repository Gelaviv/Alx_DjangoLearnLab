from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f" Book: {self.title}"
    

   
class CustomUserManager(BaseUserManager):
    def create_user (self, username, email, password =None, date_of_birth=None, profile_photo=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
            
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            profile_photo=profile_photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

        

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username,email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null= True, blank= True)
    profile_photo = models.ImageField(null= True, blank= True)

    objects = CustomUserManager()
    
    def __str__(self):
            return f" User: {self.username}"
    