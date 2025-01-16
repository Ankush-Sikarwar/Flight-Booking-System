from django.urls import path
from accounts import views
from accounts import resetPasswordView

# app_name = 'home'
urlpatterns = [
    path("/signup/", views.handelSingup, name="handelSingup"),
    path("/login", views.handleLogin, name="handleLogin"),
    path("/profile", views.profile, name="profile"),
    path("edit_profile", views.UserEditView.as_view(), name="edit_profile"),
    path("/logout", views.handleLogout, name="handleLogout"),
    # operations regarding password changes
    path("password_change", resetPasswordView.password_change, name="password_change"),
    path(
        "password_reset",
        resetPasswordView.password_reset_request,
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>",
        resetPasswordView.passwordResetConfirm,
        name="password_reset_confirm",
    ),
]
