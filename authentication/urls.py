from django.urls import path, reverse_lazy
from .views import LoginView, RegisterUserView, LogoutView
from django.contrib.auth import views as auth_views

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterUserView.as_view(), name="register"),
    path('logout/', LogoutView, name="logout"),
    path('reset/',
         auth_views.PasswordResetView.as_view(
            template_name='accounts/reset_password.html',
            email_template_name='accounts/reset_password_email.html',
            subject_template_name='accounts/reset_password_subject.txt',
            success_url = reverse_lazy('auth:password_reset_done')
         ),
         name="password_reset"),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/reset_password_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset_password_confirm.html',
            success_url = reverse_lazy('auth:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/reset_password_complete.html'
         ),
         name='password_reset_complete'),
    path('password/', auth_views.PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url = reverse_lazy('auth:password_change_done')
            ),
         name='password_change'
        ),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/change_password_done.html',
            ),
         name='password_change_done'
        )
]
