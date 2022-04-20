from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """A blog post a user is writing about."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        """Return a string represntation of the model."""
        return self.title