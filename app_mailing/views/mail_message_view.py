from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView

from app_mailing.forms import MailMessageForm
from app_mailing.models import MailMessage


class MailMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailMessage
    form_class = MailMessageForm

    def form_valid(self, form):
        new_obj: MailMessage = form.save(commit=False)
        new_obj.author = self.request.user
        new_obj.save()
        return redirect(new_obj.get_absolute_url())


class MailMessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailMessage

    def test_func(self):
        curr_user = self.request.user
        return (self.get_object().author == curr_user or
                self.request.user.has_perm('app_mailing.view_mailmessage'))


class MailMessageListView(LoginRequiredMixin, ListView):
    model = MailMessage

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_perm('app_mailing.view_mailmessage'):
            queryset.filter(author=self.request.user)
        return queryset


class MailMessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailMessage
    form_class = MailMessageForm

    def test_func(self):
        curr_user = self.request.user
        return (self.get_object().author == curr_user or
                self.request.user.has_perm('app_mailing.change_mailmessage'))


class MailMessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailMessage

    success_url = reverse_lazy('app_mailings:mail_message_list')

    def test_func(self):
        curr_user = self.request.user
        return self.get_object().author == curr_user

    def get_template_names(self):
        return 'shared/model_confirm_delete.html'
