from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from signup.models import UserProfileInfo, User
# Register your models here.

UserAdmin.list_display = ('username', 'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', )


class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ["user", "dob", "profile_pic"]
    list_display_links = ["user", "dob", "profile_pic"]
    list_filter = ["user", "dob", "profile_pic"]
    search_fields = ["user", "dob", "profile_pic"]


admin.site.register(UserProfileInfo, UserProfileInfoAdmin)

