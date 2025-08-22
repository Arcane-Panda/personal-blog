from django.db import models

# Create your models here.

class Tag(models.Model):
    word = models.CharField(max_length=35)
    
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    publicationDate = models.DateField()
    blurb = models.CharField(max_length=250)
    thumbnail = models.ImageField()
    contents = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts")
