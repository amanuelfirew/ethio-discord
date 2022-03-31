from django import forms
from .models import Room,Message
from .models import User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar','email','username','password1','password2']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        # the '__all__' accesses all the fields inside 'Room'.
        fields = '__all__'
        # exclude argument excludes 'host'and 'participants'.
        exclude = ['host','participants']
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['avatar','username','email','bio']