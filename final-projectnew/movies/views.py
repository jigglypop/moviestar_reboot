from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import MovieForm,ReviewForm
from .models import Movie,Review, Genre
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from IPython import embed
def main(request):
    return render(request,'movies/main.html')
# Create your views here.
def index(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    for movie in movies:
        cnt  = movie.audience
        title = movie.title
    context = {
        'movies':movies,
    }
    k = [0, 1, 2, 3, 4, 5, 7, 9, 11, 15]
    # for i, v in enumerate(genres):
    #     context.update({'genre'+str(i) : v})
    for kk in k:
        m = movies.filter(genre_id=Genre.objects.get(pk=kk))
        if len(m) > 20:
            m = m[0:20]
        context.update({'movie'+str(kk) : m})
    return render(request,'movies/index.html',context)
def detail(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    reviews = Review.objects.filter(movie_id=movie.pk).order_by('-id')
    if request.user.is_authenticated:
        try:
          movie_review_user = Review.objects.filter(movie_id=movie).filter(user_id=request.user)[0].user_id
        except:
          movie_review_user = -1
    else:
        movie_review_user = -1
    # embed()
    # reviews = reversed(reviews)
    review_form = ReviewForm()
    context = {
        # 'reviews':reviews,
        'movie':movie,
        'review_form':review_form,
        'movie_review_user': movie_review_user
    }
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page')
    try:
      reviews = paginator.page(page)
    except PageNotAnInteger:
      reviews = paginator.page(1)
    except EmptyPage:
      reviews = paginator.page(paginator.num_pages)
    context.update({'reviews': reviews})
    return render(request,'movies/detail.html',context)
@login_required
def review_create(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    # if request.user.is_authenticated:
    #     return redirect('accounts:login')
    # embed()
    if request.method == 'POST':
        movie_review_user = Review.objects.filter(movie_id=movie).filter(user_id=request.user)
        # embed()
        if movie_review_user:
            review = movie_review_user[0]
        else:
            review = Review()
        try:
            score = int(request.POST['star-input'][0])
        except:
            score = 0
        try:
            content = request.POST['content']
        except:
            content = ''
        # embed()
        review.content = content
        review.score = score
        review.movie_id = movie
        review.user_id = request.user
        review.save()
    return redirect('movies:detail', movie_id)
def review_delete(request,movie_id,review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('movies:detail',movie_id)
@login_required
def like(request,movie_id):
    # 좋아요를 눌렀다면
    # embed()
    if request.is_ajax():
        movie = Movie.objects.get(pk=movie_id)
        if request.user in movie.like_users.all():
            # 좋아요 취소 로직
            movie.like_users.remove(request.user)
            is_liked = False
        # 아니면
        else:
            # 좋아요 로직
            movie.like_users.add(request.user)
            is_liked = True
        context = {
            'is_liked': is_liked,
            'like_count': movie.like_users.count()
            }
        return JsonResponse(context)
    else:
        return HttpResponseForbidden()
    # movie = get_object_or_404(Movie,pk=movie_id)
    # if request.user in movie.like_users.all():
    #     movie.like_users.remove(request.user)
    # else:
    #     movie.like_users.add(request.user)
    # return redirect('movies:detail',movie_id)
@login_required
def star(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    score = int(eval(request.body.decode("utf-8"))['score'])
    # embed()
