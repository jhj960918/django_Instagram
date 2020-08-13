from django import forms
from .models import Post, CustomUser, Comment, Hashtag
# from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'hashtag_field','restaurant_location']


class SigninForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        help_texts = {
            'username': None,
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'nickname', 'phone_number' ,'profileimage']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['name']
