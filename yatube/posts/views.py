from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm
from posts.models import Group, Post, User
from yatube.settings import PAGE


def get_one_page(request, posts):
    paginator = Paginator(posts, PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    return render(
        request,
        'posts/index.html',
        {'page_obj': get_one_page(request, Post.objects.all())}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_one_page(request, posts)
    return render(
        request,
        'posts/group_list.html',
        {'page_obj': page_obj, 'group': group}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = get_one_page(request, posts)
    return render(
        request,
        'posts/profile.html',
        {'page_obj': page_obj, 'author': author}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)
