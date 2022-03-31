from django.urls import include, path
from . import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('register/',views.register,name='register'),
    path('user_profile/<int:user_id>',views.user_profile,name='user_profile'),
    path('update_user/',views.update_user,name= 'update_user'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('update_room/<int:room_id>/',views.update_room,name='update_room'),
    path('delete_room/<int:room_id>/',views.delete_room,name = 'delete_room'),
    path('delete_message/<int:room_id>/',views.delete_message,name= 'delete_message'),
    path('topics/',views.topics_page, name ="topics"),
    path('activities/',views.activity_page,name='activity'),
    path('update_message/<int:message_id>/',views.update_message,name="update_message")
]
