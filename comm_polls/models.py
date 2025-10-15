from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_polls")
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        """Returns True if poll is currently votable"""
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def has_started(self):
        """Returns True if poll start date passed"""
        return timezone.now() >= self.start_date

    @property
    def has_ended(self):
        """Returns True if poll end date passed"""
        return timezone.now() > self.end_date


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    name = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "voter")  # each user can vote only once per poll

    def __str__(self):
        return f"{self.voter} voted on {self.poll}"
