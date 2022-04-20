from django.contrib import admin
from .models import BlogPost

admin.site.site_header  = "Blog Admin"
admin.site.site_title = "Blog Admin Area"
admin.site.index_title = "Welcome to the Blog Admin"

admin.site.register(BlogPost)