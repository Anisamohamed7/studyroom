from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="login-chatbot"),  # Root path
    path("home/", views.chatbot, name="chatbot"),  # Home path for chatbot interface
    path("chat/", views.chat, name="chat"),  # Chat path
    path("chatbot/chatbot", views.chatbot_response, name="chatbot_response"),  # Chatbot response path
    # Uncomment the following if you need them for login/logout functionality:
    # path("register/", views.register, name="register"),
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
]
