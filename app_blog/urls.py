from django.urls import path

from app_blog.apps import AppBlogConfig
from app_blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = AppBlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<slug:slug>/edit', ArticleUpdateView.as_view(), name='article_update'),
    path('<slug:slug>/delete', ArticleDeleteView.as_view(), name='article_delete'),
]
