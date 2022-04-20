from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import BlogPost
from .forms import BlogPostForm


# Create your views here.
def index(request):
    """The home page for Blog."""
    return render(request, 'blogs/index.html')

#@login_required
def posts(request):
    """Show all the blogposts."""

    if request.user.is_authenticated:
        posts = BlogPost.objects.filter(owner=request.user).order_by('-date_added')

    else:
        # Show posts checked as public to unauthorized users.
        posts = BlogPost.objects.filter(publish=True).order_by('-date_added')

    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

# @login_required
def post(request, post_id):
    """Show a single post."""
    
    if request.user.is_authenticated:
        post = BlogPost.objects.get(id=post_id)
        # Ensure the post belongs to the current user.
        if post.owner != request.user:
            raise Http404
    # Show content to marked as public to unauthorized users.
    if not request.user.is_authenticated:
        try:
            post = BlogPost.objects.get(Q(id=post_id) & Q(publish=True)) 
        except BlogPost.DoesNotExist:
            raise Http404          
                   
    context = {'post': post}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        # Submit no data; create a blank form.
        form = BlogPostForm()
    else:
        # POST data submitted; process data.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:posts')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; prepopulate form with the current post.
        form = BlogPostForm(instance=post)

    else:
        # POST data submitted; process data. 
        form = BlogPostForm(instance=post, data=request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)

    context = {'post': post, 'form': form }
    return render(request, 'blogs/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """Delete/Destroy a post."""
    post = get_object_or_404(BlogPost, id=post_id)

    if post.owner != request.user:
        raise Http404

    if request.method == 'POST':
        post.delete()
        return redirect('blogs:posts')

    context = {'post': post }
    return render(request, 'blogs/delete_post.html', context)
