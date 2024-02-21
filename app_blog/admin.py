from django.contrib import admin

from app_blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date', 'is_published', )
    list_filter = ('create_date', 'is_published', )
    search_fields = ('title', 'content_text', )
