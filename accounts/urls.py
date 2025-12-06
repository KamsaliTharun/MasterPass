from django.urls import path
from accounts.views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/success/", register_success, name="register_success"),
    path("forgot_password/", forgot_password, name="forgot_password"),
    path("reset_password/", reset_password, name="reset_password"),
    path("password_reset_success/", password_reset_success, name="password_reset_success"),
]
