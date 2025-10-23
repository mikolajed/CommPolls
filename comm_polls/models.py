from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
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

    @property
    def total_votes(self):
        """Returns the total number of votes for this poll."""
        return self.poll_votes.count()


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")
    name = models.CharField(max_length=200)
    votes_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="poll_votes")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="choice_votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "voter")

    def __str__(self):
        return f"{self.voter} voted on {self.poll}"


class ManagerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_request')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manager request from {self.user.username} - {self.status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
