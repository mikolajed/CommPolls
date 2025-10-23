from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Poll, Choice, Vote, Profile, ManagerRequest
from django.utils.html import format_html

# --- Inline and Custom User Admin ---

# Unregister the default User admin before registering our custom one
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    """Displays the Profile model inline on the User admin page."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """Displays the avatar image in the admin."""
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"
    avatar_preview.short_description = 'Avatar Preview'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin that includes the Profile inline."""
    inlines = (ProfileInline,)

# --- App-specific Model Admins ---

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at", "start_date", "end_date")
    inlines = [ChoiceInline]
    list_filter = ('created_by', 'start_date', 'end_date')
    search_fields = ('name', 'description')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "poll", "votes_count")
    list_filter = ('poll',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("voter", "poll", "choice", "voted_at")
    list_filter = ('poll', 'voter')

@admin.register(ManagerRequest)
class ManagerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'requested_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
