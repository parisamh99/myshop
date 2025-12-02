from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.sessions.models import Session


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id","email", "is_superuser", "is_active", "is_verified")
    list_filter = ("is_superuser", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("email",)
    # fieldsets show us what fields we see in any of users in admin section
    fieldsets = (
        (
            "authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "permissions_group",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                    "type",
                ),
            },
        ),
        (
            "important_dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user_id","user","first_name","last_name","phone_number")
    search_fields = ("first_name", "last_name", "phone_number", "user__email")


admin.site.register(Profile,CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
admin.site.register(Session, SessionAdmin)
