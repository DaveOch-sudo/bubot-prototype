from django.urls import path

from .views import health, chat


urlpatterns = [
    path("health/", health, name="health"),
    path("chat/", chat, name="chat"),
]