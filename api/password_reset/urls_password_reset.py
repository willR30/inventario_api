from django.urls import path
from .password_reset_view import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uuid:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
