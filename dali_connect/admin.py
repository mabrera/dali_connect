from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("follows","likes",)

admin.site.register(User, UserAdmin)
admin.site.register(Post)

