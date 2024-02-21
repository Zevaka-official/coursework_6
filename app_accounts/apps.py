from django.apps import AppConfig


class AppAccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_accounts"

    verbose_name = 'Аккаунты'

    reset_password_mail_subject = 'reset password'
    verify_mail_mail_subject = 'email verify'
