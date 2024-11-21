from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
