from django.db import models
from .models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email','first_name','last_name')
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model() # User return
        fields = ('username', 'first_name', 'last_name')