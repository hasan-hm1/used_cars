from django.urls import path
from . import views as cars_views
from users import views as users_views
from django.contrib.auth import views as auth_views
from .models import Car
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', cars_views.home, name='cars-home'),
    path('home/', cars_views.home, name='cars-home-home'),
    path('car-details/<int:id>', cars_views.details, name='car-details'),
    path('sell-my-car/', cars_views.sell, name='cars-sell'),
    path('my-garage/', cars_views.my_garage, name='my-garage'),
    path('car-price/', cars_views.price, name='cars-price'),
    path('about/', cars_views.about, name='cars-about'),
    path('password-reset/', cars_views.password_reset, name='password-reset'),
    path('love-unlove-toggle/', cars_views.love_unlove, name='love-unlove-toggle'),
    path('profile/', cars_views.profile, name='profile'),
    path('register/', users_views.register, name='cars-register'),
    path('login/', users_views.login, name='cars-login'),
    path('logout/', users_views.logout, name='cars-logout'),
    # path('cars-api/', cars_views.CarsList.as_view(), name='cars-logout'),
    # related to pasword reset
#    path('password-reset/',
#          auth_views.PasswordResetView.as_view(
#              template_name='users/password_reset.html'
#          ),
#          name='password_reset'),
#     path('password-reset/done/',
#          auth_views.PasswordResetDoneView.as_view(
#              template_name='users/password_reset_done.html'
#          ),
#          name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='users/password_reset_confirm.html'
#          ),
#          name='password_reset_confirm'),
#     path('password-reset-complete/',
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='users/password_reset_complete.html'
#          ),
#          name='password_reset_complete'),  
]

urlpatterns = format_suffix_patterns(urlpatterns)
