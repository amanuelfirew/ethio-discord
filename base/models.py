from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
        """User is our own custom user model that overrides the built in user model."""
        name = models.CharField(max_length=50,null=True)
        email = models.EmailField(unique=True)
        bio = models.TextField(null=True,blank=True)
        avatar= models.ImageField(null=True,default='avatar.svg')
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    """this class creates a field for our topics"""
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Room(models.Model):
    """linking a host with the current user."""
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    """linking topics in the room with the single topic"""
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # null means if the user doesn't add a value accept a blank space as a data,
    # blank means the user can submit a blank value.
    description = models.TextField(null=True, blank=True)
    # we use related_name in ManyToManyField below because there is another 
    # attribute (host) that is linked to the User 
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    """this class is used to order the data as created and updated."""
    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.name


class Message(models.Model):
    """ linking the specific message with the user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """ linking the specific message with the room."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        if len(self.body[0:50]) < 50:
            return f'{self.body[0:50]}'
        else:
            return f'{self.body[0:50]}...'
