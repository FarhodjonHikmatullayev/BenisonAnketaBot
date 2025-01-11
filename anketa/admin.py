from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'phone', 'telegram_id')
    search_fields = ('username', 'phone', 'telegram_id')
