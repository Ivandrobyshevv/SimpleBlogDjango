from django.shortcuts import render, get_object_or_404
from . import models


def post_detail(request, id: int):
    post = get_object_or_404(models.Post, id=id, status=models.Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_list(request):
    posts = models.Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})
