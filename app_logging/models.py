from django.db import models

from app_accounts.models import User
from app_mailing.models import Mailing


class MailingReport(models.Model):
    class ReportStatus(models.IntegerChoices):
        SUCCESS = 0, 'Успешно'
        WARNING = 1, 'Предупреждение'
        FAIL = 2, 'Ошибка'

    report_date_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время отчета'
    )

    report_status = models.IntegerField(
        choices=ReportStatus.choices,
        verbose_name='Статус операции'
    )

    report_message = models.CharField(
        max_length=500,
        verbose_name='Сообщение'
    )

    mailing = models.ForeignKey(
        Mailing,
        related_name='reports',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Связанная рассылка'
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Получатель сообщения'
    )

    parent_report = models.ForeignKey(
        'MailingReport',
        on_delete=models.SET_NULL,
        null=True,
        related_name='child_reports',
    )

    def __str__(self):
        return (f'{MailingReport.ReportStatus(self.report_status).label} | '
                f'{self.report_date_time.strftime("%d %B %y %H:%M:%S")}')

    class Meta:
        verbose_name = 'Отчет рассылки'
        verbose_name_plural = 'Отчеты рассылок'
