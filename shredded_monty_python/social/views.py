from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like, SavedPost
from .forms import PostForm, CommentForm


@login_required
def social_feed(request):
    """
    Display the social feed with all posts and a post creation form.
    """
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'social_feed.html', {'posts': posts, 'form': form})


@login_required
def create_post(request):
    """
    Create a new post based on the submitted form data.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                user=request.user,
                text=form.cleaned_data['text'],
                image=form.cleaned_data.get('image'),
                video=form.cleaned_data.get('video')
            )
            return redirect('social_feed')
    return redirect('social_feed')


@login_required
def add_comment(request, post_id, parent_id=None):
    """
    Add a comment (or reply) to a post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                post=post,
                parent_id=parent_id,
                text=form.cleaned_data['text']
            )
    return redirect('social_feed')


@login_required
def like_post(request, post_id):
    """
    Toggle a like on a post.
    """
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete() # Unlike if already saved
    return redirect('social_feed')


@login_required
def save_post(request, post_id):
    """
    Toggle saving a post.
    """
    post = get_object_or_404(Post, id=post_id)
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        saved_post.delete() # Unsave if already saved
    return redirect('social_feed')
