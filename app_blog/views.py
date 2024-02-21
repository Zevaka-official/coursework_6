from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from app_blog.apps import AppBlogConfig
from app_blog.models import Article


class ArticleListView(ListView):
    model = Article
    paginate_by = AppBlogConfig.articles_per_page

    def get_queryset(self):
        if not settings.CACHE_ENABLED:

            qs = super().get_queryset()
            qs = qs.filter(is_published=True).order_by('-create_date')

            return qs

        return cache.get_or_set(
            key=f'article_list_{self.request.GET.get("page",1)}',
            default=super().get_queryset().filter(is_published=True).order_by('-create_date'),
            timeout=settings.ARTICLES_PAGE_CACHE_TIME
        )


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['popular'] = Article.objects.filter(is_published=True).filter(~Q(id=self.object.id)).order_by(
            '-view_count')[:3]
        return ctx

    def get_object(self, queryset=None):
        if not settings.CACHE_ENABLED:
            self.object = super().get_object(queryset)
            self.object.view_count += 1
            self.object.save()
        else:
            key = f'article_{self.request.path}'
            key_views = f'{key}_views'
            self.object = cache.get_or_set(
                key=key,
                default=super().get_object(queryset),
                timeout=settings.ARTICLES_PAGE_CACHE_TIME
            )

            cached_views = cache.get_or_set(
                key=key_views,
                default=1,
                timeout=50
            )
            cached_views += 1
            cache.set(key_views, cached_views)

            if cached_views >= settings.ARTICLE_CACHED_VIEW_COUNT:
                db_obj = super().get_object(queryset)
                db_obj.view_count += cached_views
                db_obj.save()
                cache.delete(key_views)
                cache.delete(key)
                self.object = db_obj

        return self.object


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content_text', 'preview_image', 'is_published')

    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.author = self.request.user
            new_obj.save()
            return redirect(reverse('app_blog:article_detail', kwargs={'slug': new_obj.slug}))


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content_text', 'preview_image', 'is_published')

    def form_valid(self, form):
        if form.is_valid():
            new_obj = form.save()
            return redirect(reverse('app_blog:article_detail', kwargs={'slug': new_obj.slug}))


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('app_blog:articles')

    def test_func(self):
        curr_user = self.request.user
        return self.get_object().mailing_owner == curr_user

    def get_template_names(self):
        return 'shared/model_confirm_delete.html'
