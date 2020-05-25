from .models import Movie,Genre,Review
from django import forms

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user_id','movie_id')
