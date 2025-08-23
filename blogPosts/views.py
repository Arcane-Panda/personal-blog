from django.shortcuts import render
from . import models
from collections import defaultdict
# Create your views here.



def index(request, page_num=0):
    #get all the blog posts for the archive tree
    #only render a subset for the main table
    #try to do so in chunks of 5. e.g page one shows 1-5, two shows 6-10, etc.
    #if there aren't enough for a full chunk, then just render whats left
    all_posts = models.BlogPost.objects.order_by("-publicationDate").all()
    count = all_posts.count()
    start = 1 + (5*page_num)

    #if our calculated start is larger than the number of blogposts,
    #we are on a page number that is too high and should return an error
    if(start > count):
        return render(request)
    
    #eg. page_num =1 should be range 6-10, but if there are only 8 total posts 
    #the range should be 6-8 
    calculatedEnd = 5 + (5*page_num)
    end = min(calculatedEnd, count)
    
    main_posts = all_posts[start:end]
    leftover = count - end
    
    #organize archive structure
    archive = defaultdict(lambda: defaultdict(list))
    for post in all_posts:
        year = post.publicationDate.year
        month = post.publicationDate.strftime("%B")
        archive[year][month].append(post)
        
    return render(request, "index.html", {"main_posts": main_posts,"archive": archive,"pageNum": page_num, "leftover": leftover})

def bio(request):
    return render(request, "bio.html")

def blogPost(request, blog_id):
    return render(request, "blog-post.html")

def search(request, searchRequest):
    return render(request, "search-results.html")