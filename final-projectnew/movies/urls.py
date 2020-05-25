from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('',views.main,name='main'),
    path('index/',views.index,name='index'),
    path('<int:movie_id>/',views.detail,name='detail'),
    path('<int:movie_id>/create/',views.review_create,name='review_create'),
    path('<int:movie_id>/create/<int:review_id>/delete/',views.review_delete,name='review_delete'),
    path('<int:movie_id>/like/',views.like,name='like'),
    path('<int:movie_id>/stars/',views.star,name='stars'),
]
