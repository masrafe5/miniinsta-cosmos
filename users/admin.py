from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html, mark_safe
from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display   = ['avatar_tag', 'username', 'email', 'role_badge', 'is_staff', 'is_active', 'date_joined']
    list_display_links = ['username']
    list_filter    = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields  = ['username', 'email', 'first_name', 'last_name']
    ordering       = ['-date_joined']
    list_per_page  = 25

    fieldsets = UserAdmin.fieldsets + (
        ('MiniInsta Profile', {
            'fields': ('role', 'bio', 'profile_picture', 'website', 'location')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MiniInsta', {'fields': ('role', 'email')}),
    )

    @admin.display(description='')
    def avatar_tag(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;">',
                obj.profile_picture.url
            )
        initials = obj.username[0].upper() if obj.username else '?'
        return format_html(
            '<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#4f46e5);'
            'display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;">'
            '{}</div>',
            initials
        )

    @admin.display(description='Role')
    def role_badge(self, obj):
        if obj.role == 'creator':
            return mark_safe(
                '<span style="background:rgba(192,132,252,.15);color:#c084fc;border:1px solid rgba(192,132,252,.4);'
                'padding:2px 10px;border-radius:99px;font-size:11px;font-weight:600;">Creator</span>'
            )
        return mark_safe(
            '<span style="background:rgba(45,212,191,.1);color:#2dd4bf;border:1px solid rgba(45,212,191,.3);'
            'padding:2px 10px;border-radius:99px;font-size:11px;font-weight:600;">Consumer</span>'
        )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display  = ['follower', 'following', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['follower__username', 'following__username']
    ordering      = ['-created_at']
    list_per_page = 30
