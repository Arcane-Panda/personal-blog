from django.shortcuts import render
from . import models
# Create your views here.



def index(request):
    return render(request, "index.html")

def bio(request):
    return render(request, "bio.html")

def blogPost(request, blog_id):
    return render(request, "blog-post.html")

def search(request, searchRequest):
    return render(request, "search-results.html")