from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at", "start_date", "end_date")
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "poll", "vote_count")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("voter", "poll", "choice", "voted_at")
