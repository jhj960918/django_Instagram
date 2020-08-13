from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
# Create your models here.

class Post(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="writer", default="")
    
    hashtag_field = models.CharField(max_length=200, blank=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True)
    restaurant_location = models.CharField(max_length=200,blank=True)
    create_date = models.DateTimeField('date published',blank=True ,default=datetime.now())#게시물 등록후 지난 시간을 나타내는 필드
    

    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="like_user_set", through="Like")

    @property
    def like_count(self):
        return self.like_user_set.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('user', 'post')
        )


class Hashtag(models.Model):
    def __str__(self):
        return self.related_name

    name = models.CharField(max_length=50)


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
    
    nickname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    profileimage = models.ImageField(upload_to='images/', blank=True)

class Comment(models.Model):
    def __str__(self):
        return self.text
    c_writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="c_writer", default="")
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=50)
    class Meta:
        ordering = ['-id']
            
    def __str__(self):
        return '%s - %s' % (self.c_writer, self.text) 
