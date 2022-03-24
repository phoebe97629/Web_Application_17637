from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    bio = models.CharField(max_length = 2000)
    user = models.OneToOneField(User, on_delete = models.PROTECT)
    picture = models.FileField(blank = True)
    content_type = models.CharField(max_length = 50, blank = True)
    following = models.ManyToManyField(User, related_name = 'followers')


    def __str__(self):
        return "Post by:" + self.user



class Post(models.Model):
    text = models.CharField(max_length = 2000)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_time = models.DateTimeField()

    def __str__(self):
        return "Post by:" + self.created_by+" "+self.text +" " + self.created_time






