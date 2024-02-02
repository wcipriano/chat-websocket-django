# chat/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('<str:room_name>/', views.room_view, name='chat-room'),
    path('<str:room_name>/send-test/', views.send_test, name='send-test-message'),
]
