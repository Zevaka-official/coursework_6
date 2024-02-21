from django.db import models
from django.urls import reverse_lazy

from app_accounts.models import User


class MailMessage(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mailing_messages',
        verbose_name='Автор сообщения'
    )

    subject = models.CharField(
        max_length=150,
        verbose_name='Тема письма'
    )

    text = models.TextField(
        max_length=1024,
        verbose_name='Текст письма'
    )

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse_lazy('app_mailings:mail_message_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Mailing(models.Model):
    class PeriodicityChoice(models.IntegerChoices):
        DAILY = 0, 'Ежедневно'
        WEEKLY = 1, 'Еженедельно'
        MONTHLY = 2, 'Ежемесячно'

    class MailingStatusChoice(models.IntegerChoices):
        CREATED = 0, 'Создана'
        STARTED = 1, 'Запущена'
        FINISHED = 2, 'Завершена'
        STOPPED = 3, 'Остановлена'

    mailing_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Владелец рассылки'
    )

    date_start = models.DateField(
        auto_now=False,
        verbose_name='Дата начала рассылки'
    )

    date_finish = models.DateField(
        auto_now=False,
        verbose_name='Дата окончания рассылки'
    )

    periodicity = models.IntegerField(
        choices=PeriodicityChoice.choices,
        default=PeriodicityChoice.DAILY,
        verbose_name='Периодичность рассылки'
    )

    mailing_status = models.IntegerField(
        choices=MailingStatusChoice.choices,
        default=MailingStatusChoice.CREATED,
        verbose_name='Статус рассылки'
    )

    attempts_count = models.PositiveIntegerField(
        default=1,
        verbose_name='Число повторных попыток',
        help_text='Количество попыток повторной отправки в случае неудачи'
    )

    message = models.ForeignKey(
        MailMessage,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Рассылаемое сообщение'
    )

    subscribers = models.ManyToManyField(
        User,
        related_name='subscriptions',
        verbose_name='Получатели'
    )

    def __str__(self):
        return (
            f'{self.message.subject} от '
            f'{self.date_start.strftime("%d %B %Y")} | '
            f'{Mailing.PeriodicityChoice(self.periodicity).label} | '
            f'{Mailing.MailingStatusChoice(self.mailing_status).label}'
        )

    def get_absolute_url(self):
        return reverse_lazy('app_mailings:mailing_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('can_stop_mailing', 'Может остановить рассылку')
        ]


class MailingResend(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Получатель'
    )

    attempts_left = models.IntegerField(
        default=1,
        verbose_name='Оставшееся число попыток'
    )

    def __str__(self):
        return f'{self.mailing} ({self.recipient.email})'

    class Meta:
        verbose_name = 'Повторная отправка'
        verbose_name_plural = 'Список писем для повторной отправки'
        unique_together = ('mailing', 'recipient')
