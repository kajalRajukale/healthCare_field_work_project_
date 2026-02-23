from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).select_related('author', 'category')
    categories = BlogCategory.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views_count += 1
    post.save(update_fields=['views_count'])
    return render(request, 'blog/blog_detail.html', {'post': post})
