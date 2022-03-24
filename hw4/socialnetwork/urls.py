from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_action, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('global', views.global_action, name='global'),
    path('follower', views.follower_action, name='follower'),
    path('my_profile', views.my_profile_action, name = 'my_profile'),
    path('follower_profile', views.follower_profile_action, name='follower_profile'),
]

