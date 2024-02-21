from app_accounts.apps import AppAccountsConfig
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from app_accounts.views import UserDetailView, UserResetPassword, UserEmailVerify, UserCreateView, UserEditView, \
    VerifyMailAgain, UserPasswordChangeView, UserListView, UserBlockUnblockView

app_name = AppAccountsConfig.name

urlpatterns = [
    path('', UserDetailView.as_view(), name='user_detail'),
    path('list/', UserListView.as_view(), name='users_list'),
    path('<int:pk>/block/', UserBlockUnblockView.as_view(), name='user_block'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('registration/email_verify/<uidb64>/<token>/', UserEmailVerify.as_view(), name='email_verify'),
    path('registration/email_verify/resend', VerifyMailAgain.as_view(), name='email_verify_again'),
    path('reset_password/', UserResetPassword.as_view(), name='reset_password'),
    path('edit/', UserEditView.as_view(), name='user_edit'),
    path('password/', UserPasswordChangeView.as_view(), name='change_password'),

    path('login/', LoginView.as_view(
        template_name='app_accounts/login.html',
    ),
         name='login',
         ),

    path('registration/email_verify/', TemplateView.as_view(
        template_name='app_accounts/user_email_verify.html',
    ),
         name='email_verify_alert'
         ),

    path('registration/email_verify_failed/', TemplateView.as_view(
        template_name='app_accounts/user_email_verify_failed.html',
    ),
         name='email_verify_failed'
         ),

    path('reset_password/success', TemplateView.as_view(
        template_name='app_accounts/reset_password_success.html',
    ),
         name='reset_password_alert'
         ),
]
