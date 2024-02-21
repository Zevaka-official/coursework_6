from django.conf import settings
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render

from app_blog.models import Article
from app_mailing.models import Mailing


def e_handler403(request, exception):
    return render(request, 'shared/errors/403.html', status=403)


def e_handler404(request, exception):
    return render(request, 'shared/errors/404.html', status=404)


def index_page_view(request, *args, **kwargs):
    return render(request, 'landing/index.html', context={
        'popular_articles': Article.objects.order_by('-view_count')[:settings.POPULAR_ARTICLES_COUNT],
        'active_mailing': len(Mailing.objects.filter(mailing_status=Mailing.MailingStatusChoice.STARTED)),
        'total_mailing': len(Mailing.objects.filter(~Q(mailing_status=Mailing.MailingStatusChoice.STOPPED)))
    })
