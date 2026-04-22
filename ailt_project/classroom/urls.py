from django.urls import path
from . import views

urlpatterns = [
    path('', views.classroom_ui, name='classroom_ui'),
    path('api/chat/', views.chat_with_ailt, name='chat_with_ailt'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('presentation/', views.presentation_ui, name='presentation_ui'),
    path('api/presentation-chat/', views.presentation_chat, name='presentation_chat'),
]