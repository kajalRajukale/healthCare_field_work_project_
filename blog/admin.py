from django.contrib import admin
from .models import BlogPost, BlogCategory


@admin.register(BlogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'created_at']
    list_filter = ['is_published', 'category']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
