from django.shortcuts import render
from . import models
from collections import defaultdict
# Create your views here.

#helper function that packages all the blog posts into a dictionary
#sorted chronologically by month/year
def getArchiveDict():
    all_posts = models.BlogPost.objects.order_by("-publicationDate").all()
    archive_dict = defaultdict(lambda: defaultdict(list))
    for post in all_posts:
        year = post.publicationDate.year
        month = post.publicationDate.strftime("%B")
        archive_dict[year][month].append(post)
     
    # Convert to normal dicts and sort
    archive = {
        year: {
            month: posts
            for month, posts in sorted(months.items(), key=lambda m: m[0], reverse=True)
        }
        for year, months in sorted(archive_dict.items(), key=lambda y: y[0], reverse=True)
    }
    return archive


#view for the main page of the site, which displays blog posts and lets you paginate through them
def index(request, page_num=0):
    #only showing a subset a subset of blogposts
    #each page shows a chunk of 5. e.g page one shows 1-5, two shows 6-10, etc.
    #if there aren't enough for a full chunk, then just render whats left 
    all_posts = models.BlogPost.objects.order_by("-publicationDate").all()
    count = all_posts.count()
    start =  5*page_num

    #if our calculated start is larger than the number of blogposts,
    #we are on a page number that is too high and should return an error. 
    if(start > count):
        return render(request, "error-page.html")
    
    #eg. page_num =1 should be range 6-10, but if there are only 8 total posts 
    #the range should be 6-8 
    calculatedEnd = 4 + (5*page_num)
    end = min(calculatedEnd, count)
    
    main_posts = all_posts[start:end]
    
    leftover = count - end
    
    archive = getArchiveDict()
    
    olderPage = page_num + 1
    newerPage = page_num - 1
    
    allTags = models.Tag.objects.order_by("word").all()
    return render(request, "index.html", {"main_posts": main_posts,"archive": archive,"pageNum": page_num, 
                                          "olderPage": olderPage, "newerPage": newerPage , "leftover": leftover,
                                          "allTags": allTags})


#view for the "About Me" page. this is basically all static content
def bio(request):
    archive = getArchiveDict()
    allTags = models.Tag.objects.order_by("word").all()
    return render(request, "bio.html", {"archive": archive, "allTags": allTags})


#view for the "My Projects" page. this is basically all static content
def myProjects(request):
    archive = getArchiveDict()
    allTags = models.Tag.objects.order_by("word").all()
    return render(request, "my-projects.html", {"archive": archive, "allTags": allTags})

#view for any blog post. gets the blog object from the database and renders it
def blogPost(request, blog_id):   
    archive = getArchiveDict()
    allTags = models.Tag.objects.order_by("word").all()
    
    #since the blog id is in the url, make sure it corresponds to an existing blog post
    try:
        post = models.BlogPost.objects.get(id=blog_id)
    except:
        return render(request, "error-page.html")
    
    previous = -1
    next = -1
    
    if(models.BlogPost.objects.filter(id=blog_id-1).exists()):
        previous = blog_id-1
    if(models.BlogPost.objects.filter(id=blog_id+1).exists()):
        next = blog_id+1
    return render(request, "blog-post.html", {"post": post, "archive": archive, "allTags": allTags, "previous": previous, "next": next})

#view for the search page, searches the database for blogs that have matching titles, content, or tags,
#then sends the results to be displayed 
def search(request):
    archive = getArchiveDict()
    allTags = models.Tag.objects.order_by("word").all()
    
    searchQuery = request.GET.get("q")
    if searchQuery!="":   
        titleMatches = models.BlogPost.objects.filter(title__icontains=searchQuery)
        contentMatches = models.BlogPost.objects.filter(contents__icontains=searchQuery)
        tagMatches = models.BlogPost.objects.filter(tags__word__icontains=searchQuery)
        results = titleMatches.union(contentMatches,tagMatches).order_by("-publicationDate").all()  
        return render(request, "search-results.html", {"archive": archive, "allTags": allTags, "results": results, "query": searchQuery, "numResults": results.count()})
    
    return render(request, "search-results.html", {"archive": archive, "allTags": allTags, "numResults": 0})

