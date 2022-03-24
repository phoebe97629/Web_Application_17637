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
    path('unfollow/<int:user_id>', views.unfollow, name = 'unfollow'), 
    path('other_profile/<int:user_id>', views.other_profile, name = 'other_profile'), 
    path('fetch', views.other_profile, name = 'fetch'), 
    path('follow/<int:user_id>', views.follow, name = 'follow'), 
    # path('comments', views.add_comment, name = 'comments'), 
    path('add-item', views.add_item, name='ajax-add-item'),
    path('get-global', views.get_list_json_dumps_serializer),
    path('add-comment', views.add_comment_item, name='add-comment'),
    path('get-follower', views.get_list_follower), 
    path('add-follower-comment', views.add_follower_comment_item, name = 'add-follower-comment'),

]

