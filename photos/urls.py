from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.feed,               name='feed'),
    path('upload/',                   views.upload_photo,       name='upload_photo'),
    path('photo/<int:pk>/',           views.photo_detail,       name='photo_detail'),
    path('photo/<int:pk>/comment/',   views.add_comment,        name='add_comment'),
    path('photo/<int:pk>/rate/',      views.rate_photo,         name='rate_photo'),
    path('photo/<int:pk>/like/',      views.like_photo,         name='like_photo'),
    path('photo/<int:pk>/edit/',      views.edit_photo,         name='edit_photo'),
    path('photo/<int:pk>/delete/',    views.delete_photo,       name='delete_photo'),
    path('photo/<int:pk>/save/',      views.toggle_save_photo,  name='toggle_save_photo'),
    path('comment/<int:pk>/delete/',  views.delete_comment,     name='delete_comment'),
    path('dashboard/',                views.creator_dashboard,  name='creator_dashboard'),
    path('dashboard/consumer/',       views.consumer_dashboard, name='consumer_dashboard'),
]
