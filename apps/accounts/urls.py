from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.views import PasswordChangeView, LoginView


app_name = 'accounts'

urlpatterns = [

    # Mateus
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Implementações duvidosas (anteriores)
    path('password_reset/',auth_views.PasswordResetView.as_view(), name="password_reset_form" ),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done" ),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm" ),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete" ),
]
