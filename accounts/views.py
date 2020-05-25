from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import User
from movies.models import Review, Movie, Genre
from django.contrib.auth.decorators import login_required




def indexs(request):
    Users = User.objects.all()
    context = {
        'Users':Users
    }
    return render(request,'accounts/indexs.html',context)

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/signup.html',context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/login.html',context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def profile(request, account_pk):
    User = get_user_model()
    user = get_object_or_404(User,pk=account_pk)
    context = {
        'user_profile':user
    }
    genres_score = [0] * 21
    counts = [0] * 21
    reviews = user.review_set.order_by('-score')
    for review in reviews:
      genres_score[review.movie_id.genre_id.id] += review.score
      counts[review.movie_id.genre_id.id] += 1
    ## 장르별 평균점수 계산
    avg_genre = [0] * 21
    for i in range(len(avg_genre)):
      if counts[i] == 0:
        continue
      avg_genre[i] = int(genres_score[i]/counts[i])
    genre = avg_genre.index(max(avg_genre))  # 장르별 점수 최고점
    movies = Movie.objects.filter(genre_id_id=genre).order_by('-audience')
    user_watch_movie = set()
    for r in user.review_set.all():
      user_watch_movie.add(r.movie_id)
    my_movies = []
    if not user_watch_movie:
      genres = Genre.objects.all()
      my_movies = genres[0].movie_set.all()
    else:
      for movie in movies:
        if movie in user_watch_movie:
          continue
        my_movies.append(movie)
        if len(my_movies) == 10:
          break
    context.update({'my_movies': my_movies})
    return render(request,'accounts/profile.html',context)

def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User,pk=account_pk)
    if obama != request.user:
        if request.user in obama.followers.all():
            obama.followers.remove(request.user)
        else:
            obama.followers.add(request.user)
        return redirect('accounts:profile',account_pk)

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user) # 반드시 첫번째 인자로 user
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)