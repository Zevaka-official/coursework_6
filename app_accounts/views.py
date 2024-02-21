from django.contrib.auth import login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, FormView, ListView
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode

from app_accounts.forms import UserResetPasswordForm, UserRegisterForm, UserEditForm, UserBlockUnblockForm
from app_accounts.models import User
from app_accounts.services import send_email_to_verify, send_new_user_password


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    login_url = reverse_lazy('app_accounts:login')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Информация об аккаунте'
        return ctx

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User

    def test_func(self):
        curr_user = self.request.user
        return any([
            curr_user.has_perm('app_accounts.view_user'),
            curr_user.has_perm('app_accounts.can_block_users')
        ])


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'app_accounts/register.html'
    success_url = reverse_lazy('app_accounts:login')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            login(self.request, self.object)
            send_email_to_verify(self.object.id, get_current_site(self.request).id)
            return redirect(reverse_lazy('app_accounts:email_verify_alert'))

        return self.render_to_response(self.get_context_data(form=form))


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'app_accounts/user_edit.html'
    success_url = reverse_lazy('app_accounts:user_detail')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            return redirect(reverse_lazy('app_accounts:user_detail'))
        return self.render_to_response(self.get_context_data(form=form))


class UserPasswordChangeView(PasswordChangeView):
    form_class = SetPasswordForm
    template_name = 'app_accounts/user_password_change.html'

    def get_success_url(self):
        return reverse_lazy('app_accounts:user_detail')


class UserEmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_email_verify = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy('app_accounts:user_detail'))
        return redirect(reverse_lazy('app_accounts:email_verify_failed'))

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class VerifyMailAgain(LoginRequiredMixin, View):
    login_url = reverse_lazy('app_accounts:login')

    def get(self, request):
        send_email_to_verify(request.user.id, get_current_site(request).id)
        return redirect(reverse_lazy('app_accounts:email_verify_alert'))


class UserResetPassword(FormView):
    form_class = UserResetPasswordForm
    template_name = 'app_accounts/reset_password.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Сброс пароля'
        return ctx

    def form_valid(self, form):
        if form.is_valid():
            email = form.data['user_email']
            new_password = User.objects.make_random_password()
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            send_new_user_password(user.id, new_password, get_current_site(self.request).id)

            return redirect(reverse_lazy('app_accounts:reset_password_alert'))


class UserBlockUnblockView(UpdateView):
    model = User
    template_name = 'app_accounts/user_edit.html'
    form_class = UserBlockUnblockForm

    def get_success_url(self):
        return reverse_lazy('app_accounts:users_list')
