from django.apps import AppConfig
from config.settings import env


class AppBlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_blog"
    verbose_name = "Блог"

    articles_per_page = env.int('ARTICLES_PER_PAGE', 15)
