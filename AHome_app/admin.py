from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Design, Like, Comment, Follow, OverlayLog, CustomUser

admin.site.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Design)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(OverlayLog)

