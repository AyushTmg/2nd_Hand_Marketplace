from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display=['first_name','last_name','email','username', 'image',"is_staff", "is_active","is_superuser","last_login","date_joined"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name","last_name","username","email",'image', "password1", "password2", "is_staff",
                "is_active","is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
