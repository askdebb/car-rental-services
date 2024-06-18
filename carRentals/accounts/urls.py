from django.urls import path
from .views import login_view, logout_view, register, forgot_password, profile, reset_password_confirm

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('profile/', profile, name='profile'),
    path('reset-password-confirm/<str:token>/', reset_password_confirm, name='reset_password_confirm'),
]
