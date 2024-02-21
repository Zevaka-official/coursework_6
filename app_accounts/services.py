import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator

from app_accounts.apps import AppAccountsConfig
from app_accounts.cronjobs import background_task_manager
from app_accounts.models import User

logger = logging.getLogger(__name__)


@background_task_manager.schedule(
    retry_count=settings.ACCOUNT_SERVICE_MAIL_RETRY_COUNT,
    ttl=settings.ACCOUNT_SERVICE_MAIL_TASK_TTL)
def send_email_to_verify(user_id: int, site_id: int):
    try:
        user = User.objects.get(pk=user_id)
        site = Site.objects.get(pk=site_id)

        uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        domain_name = site.domain
        domain_scheme = 'http'  # TODO: hardcoded scheme!
        uri = reverse('app_accounts:email_verify', kwargs={'uidb64': uid_b64, 'token': token})

        ctx = {
            'user': user,
            'email_verify_uri': f"{domain_scheme}://{domain_name}{uri}",
        }

        html_body = render_to_string('shared/email/email_verify.html', context=ctx)

        msg = EmailMultiAlternatives(
            subject=AppAccountsConfig.verify_mail_mail_subject,
            to=[user.email]
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        logger.debug(f'Send verify mail to {user.email} complete')

    except Exception as e:
        logger.error(e)


@background_task_manager.schedule(
    retry_count=settings.ACCOUNT_SERVICE_MAIL_RETRY_COUNT,
    ttl=settings.ACCOUNT_SERVICE_MAIL_TASK_TTL)
def send_new_user_password(user_id: int, new_password: str, site_id: int):
    try:
        user = User.objects.get(pk=user_id)
        site = Site.objects.get(pk=site_id)

        ctx = {
            'user': user,
            'new_password': new_password,
        }

        html_body = render_to_string('shared/email/email_reset_password.html', context=ctx)

        msg = EmailMultiAlternatives(
            subject=AppAccountsConfig.reset_password_mail_subject,
            to=[user.email]
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        logger.debug(f'Send new password mail to {user.email} complete')

    except Exception as e:
        logger.error(e)
