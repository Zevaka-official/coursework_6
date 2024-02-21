from app_mailing.apps import AppMailingConfig
from django.urls import path

from app_mailing.views import (MailingCreateView, MailingDetailView, MailingListView, MailingUpdateView,
                               MailingDeleteView,
                               MailMessageCreateView, MailMessageDetailView, MailMessageListView, MailMessageUpdateView,
                               MailMessageDeleteView, MailingStopView)

app_name = AppMailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/stop', MailingStopView.as_view(), name='mailing_stop'),

    path('mail_messages/', MailMessageListView.as_view(), name='mail_message_list'),
    path('mail_messages/create/', MailMessageCreateView.as_view(), name='mail_message_create'),
    path('mail_messages/<int:pk>/', MailMessageDetailView.as_view(), name='mail_message_detail'),
    path('mail_messages/<int:pk>/update', MailMessageUpdateView.as_view(), name='mail_message_update'),
    path('mail_messages/<int:pk>/delete', MailMessageDeleteView.as_view(), name='mail_message_delete'),
]
