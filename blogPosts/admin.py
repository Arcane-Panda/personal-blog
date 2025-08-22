from django.contrib import admin
from .models import Tag, BlogPost
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    list_display = ["word"]
    
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "publicationDate"]

admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost,BlogPostAdmin)
