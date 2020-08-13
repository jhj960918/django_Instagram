from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, CustomUser, Hashtag
from .forms import PostForm, SigninForm, UserForm, CommentForm, HashtagForm
from django.template.loader import render_to_string
# from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse
import json
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.


def main(request):
    posts = Post.objects.all().order_by('-id')
    # users = User.objects.all()
    signin_form = SigninForm()
    comment_form = CommentForm()
    userList =CustomUser.objects.all().order_by('-id')
    paginator = Paginator(userList,5)
    page = request.GET.get('page')
    pages =  paginator.get_page(page)
    return render(request, 'appname/main.html', {'posts': posts,'userList':userList,'pages':pages, 'signin_form': signin_form, 'comment_form': comment_form})


def create(request):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.create_date = timezone.datetime.now()
            hashtag_field = form.cleaned_data['hashtag_field']
            restaurant_location = form.cleaned_data['restaurant_location']
            str_hashtags = hashtag_field.split('#')
            list_hashtags = list()

            for hashtag in str_hashtags:
                if Hashtag.objects.filter(name=hashtag):
                    list_hashtags.append(Hashtag.objects.get(name=hashtag))
                else:
                    temp_hashtag = HashtagForm().save(commit=False)
                    temp_hashtag.name = hashtag
                    temp_hashtag.save()
                    list_hashtags.append(temp_hashtag)

            post.save()
            post.hashtags.add(*list_hashtags)
            return redirect('main')
    else:
        form = PostForm()
        return render(request, 'appname/create.html', {'form': form})


def read(request):
    return redirect('main')


def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('main')
    else:
        form = PostForm(instance=post)
        return render(request, 'appname/create.html', {'form': form})


def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('main')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패. 다시 시도해보세요")
    else:
        signin_form = SigninForm()
        return render(request, 'appname/signin.html', {'signin_form': signin_form})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
                                                      email=form.cleaned_data['email'],
                                                      password=form.cleaned_data['password'],
                                                      nickname=form.cleaned_data['nickname'],
                                                      phone_number=form.cleaned_data['phone_number'],
                                                      profileimage=request.FILES['profileimage'])
            login(request, new_user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'appname/signup.html', {'form': form})


def hashtag(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    return render(request, 'appname/hashtag.html', {'hashtag': hashtag})


def mypage(request):
    posts = Post.objects.all().order_by('-id')
    signin_form = SigninForm()
    comment_form = CommentForm()
    return render(request, 'appname/mypage.html', {'posts': posts, 'signin_form': signin_form, 'comment_form': comment_form})


def post_like(request):
    pk = request.POST.get('pk', None)  # ajax 통신을 통해서 template에서 POST방식으로 전달
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(
        user=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message': message
               }

    return HttpResponse(json.dumps(context), content_type="application/json")
    # context를 json 타입으로


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'appname/main.html', {'object_list': posts})


def comment(request, post_id):
    if not request.user.is_active:
        return HttpResponse("Can't write a comment without Sign In")
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.c_writer = request.user
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('main')


def kakao_map(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    return render(request, 'appname/kakao_map.html', {'post': post})
