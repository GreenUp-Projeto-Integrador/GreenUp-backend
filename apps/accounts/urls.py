from django.urls import path
from .views import AccountSummaryView, ChangePasswordView, MeView, UserStatusView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("me/summary/", AccountSummaryView.as_view(), name="account_summary"),
    path("<int:pk>/<str:action>/", UserStatusView.as_view(), name="user_status"),
]
