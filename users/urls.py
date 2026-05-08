from django.urls import path
from . import views

urlpatterns = [
    path('register/',         views.register_consumer, name='register'),
    path('login/',            views.login_view,         name='login'),
    path('logout/',           views.logout_view,        name='logout'),
    path('profile/',          views.profile_view,       name='profile'),
    path('profile/edit/',     views.edit_profile,       name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('follow/<str:username>/',  views.follow_user,  name='follow_user'),
    path('create-creator/',   views.create_creator,     name='create_creator'),
    path('explore/',          views.explore_users,      name='explore_users'),
]
