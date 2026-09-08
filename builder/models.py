from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return f"{self.name} ({self.type})"


class Website(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='website')
    website_title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    about_section = models.TextField(blank=True)
    services = models.JSONField(default=list, blank=True)
    slug = models.TextField(help_text="Generated full HTML markup", blank=True)
    status = models.CharField(max_length=50, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Website: {self.website_title} for {self.business.name}"
