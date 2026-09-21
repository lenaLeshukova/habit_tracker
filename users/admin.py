from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'telegram_chat_id', 'is_staff', 'is_active')
    search_fields = ('email', 'telegram_chat_id')
