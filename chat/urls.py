from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
# This is the initial URL patterns file for the chat application. You define the course_chat_room URL pattern, including the course_id parameter with the int prefix,as you only expect an integer value here
    path('room/<int:course_id>/', views.course_chat_room,
         name='course_chat_room'),
]
