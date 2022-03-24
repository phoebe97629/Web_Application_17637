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
    path('get_photo/<int:id>', views.get_photo, name = 'get_photo'),
    path('add-post', views.post, name = 'add-post'),
    path('unfollow/<int:user_id>', views.unfollow, name = 'unfollow'), 
    path('other_profile/<int:user_id>', views.other_profile, name = 'other_profile'), 
    path('fetch', views.other_profile, name = 'fetch'), 
    path('follow/<int:user_id>', views.follow, name = 'follow')

]

