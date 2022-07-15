from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from .utils import slug_generator

class BlogPost(models.Model):
    """A blog post a user is writing about."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Return a string represntation of the model."""
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogs:post_detail', kwargs={"slug": self.slug})


def blogpost_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slug_generator(instance, save=False)

pre_save.connect(blogpost_pre_save, sender=BlogPost)


def blogpost_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slug_generator(instance, save=True)

post_save.connect(blogpost_post_save, sender=BlogPost)


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"