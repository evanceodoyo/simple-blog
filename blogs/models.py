from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """A blog post a user is writing about."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ['-date_added']

    def __str__(self):
        """Return a string represntation of the model."""
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ['-created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"