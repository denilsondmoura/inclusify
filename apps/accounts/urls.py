from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.views import AccountLoginView, AccountRegisterView, AccountPasswordResetView, AccountPasswordResetDoneView, \
    AccountPasswordResetConfirmView, AccountPasswordResetCompleteView, AccountProfileDetailView, AccountProfileEditView, \
    AccountProfileView, account_logout


app_name = 'accounts'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('register/', AccountRegisterView.as_view(), name='register'),
    path("logout/", account_logout, name="logout"),
    
    path("password_reset/", AccountPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", AccountPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", AccountPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", AccountPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path("profile/", AccountProfileView.as_view(), name="profile_detail"),
    path("profile/edit", AccountProfileEditView.as_view(), name="profile_edit"),
]
