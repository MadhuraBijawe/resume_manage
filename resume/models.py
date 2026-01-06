from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    location = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resume(models.Model):  # ✅ Merged version
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=100)
    skills = models.TextField()
    file = models.FileField(upload_to='resumes/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
