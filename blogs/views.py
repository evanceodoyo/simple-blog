from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm


# Create your views here.
def index(request):
    """The home page for Blog."""
    return render(request, 'blogs/index.html')

#@login_required
def posts(request):
    """Show the blogposts."""  
    if request.user.is_authenticated:
        posts = BlogPost.objects.filter(Q(owner=request.user) | Q(publish=True)).order_by('-date_added')

    else:
        # Show posts checked as public to unauthenticated users.
        posts = BlogPost.objects.filter(publish=True).order_by('-date_added')
        
    search_post = request.GET.get('search')
    if search_post:
        if request.user.is_authenticated:
            posts = BlogPost.objects.filter(Q(owner=request.user) | Q(publish=True)).filter(Q(title__icontains=search_post) | Q(text__icontains=search_post) |Q(owner__username__contains=search_post)) 
        else:
            posts = posts.filter(Q(title__icontains=search_post) | Q(text__icontains=search_post) |Q(owner__username__contains=search_post)).exclude(publish=False)   
                
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)

# @login_required
def post_detail_view(request, slug=None):
    """Show a single post and the comment section."""
    post = None
    if slug is not None:
        try:
            if request.user.is_authenticated:
                post = BlogPost.objects.get(Q(slug=slug), Q(owner=request.user) | Q(publish=True))
                
                # Restricting access to private post.
                if not post.publish and request.user != post.owner:
                    raise Http404   
            else:
                post = BlogPost.objects.get(Q(slug=slug), Q(publish=True))

        except BlogPost.DoesNotExist:
            raise Http404 

    comments = Comment.objects.filter(post=post).filter(active=True)                   
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url(), slug=post.slug)
        
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }    

    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new post."""
    if request.method == 'POST':
        # POST data submitted; process data.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect(new_post.get_absolute_url())
    else:
        # Submit no data; create a blank form.
        form = BlogPostForm()
        
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, slug):
    """Edit an existing post."""
    post = get_object_or_404(BlogPost, slug=slug)

    if post.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # POST data submitted; process data. 
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url(), slug=post.slug)

    else:
        # Initial request; prepopulate form with the current post.
        form = BlogPostForm(instance=post)

    context = {'post': post, 'form': form }
    return render(request, 'blogs/edit_post.html', context)

@login_required
def delete_post(request, slug):
    """Delete/Destroy a post."""
    post = get_object_or_404(BlogPost, slug=slug)

    if post.owner != request.user:
        raise Http404

    if request.method == 'POST':
        post.delete()
        return redirect('blogs:posts')

    context = {'post': post }
    return render(request, 'blogs/delete_post.html', context)
