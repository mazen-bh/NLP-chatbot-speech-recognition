from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="chatbot"),
    path('chatbotResponse/', views.chatbotResponse, name="chatbotResponse"),
    path('soundResponse/', views.soundResponse, name="soundResponse"),

]

