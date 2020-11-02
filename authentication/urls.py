from django.urls import path
from .views import LoginView, RegisterUserView, PasswordResetRequestView, LogoutView
from django.contrib.auth.views import PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterUserView.as_view(), name="register"),
    path('logout/', LogoutView, name="logout"),
    path('password_reset/', PasswordResetRequestView.as_view(),
         name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/reset_password_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='accounts/reset_password_complete.html'),
         name='password_reset_complete'),
]
