from django.contrib import admin
from .models import BlogPost, Comment

admin.site.site_header  = "Blog Admin"
admin.site.site_title = "Blog Admin Area"
admin.site.index_title = "Welcome to the Blog Admin"

class CommentInline(admin.StackedInline):
    model = Comment

class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'owner', 'text', 'publish']}), 
    ]
    inlines = [CommentInline]
    list_display =('title', 'slug', 'owner', 'date_added', 'date_updated', 'publish')
    search_fields = ['title', 'text']
    list_filter = ['date_added', 'title', 'owner', 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['disapprove_comments', 'approve_comments']

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)