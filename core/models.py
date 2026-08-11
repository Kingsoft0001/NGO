from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.conf import settings
import os

# Ensure the custom directories exist
os.makedirs(settings.BACKGROUND_DIR, exist_ok=True)
os.makedirs(settings.GALLERY_DIR, exist_ok=True)

background_storage = FileSystemStorage(location=settings.BACKGROUND_DIR, base_url='/media/background/')
gallery_storage = FileSystemStorage(location=settings.GALLERY_DIR, base_url='/media/gallery/')

class SiteSettings(models.Model):
    name = models.CharField(max_length=200, default="NGO Name")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    home_background_image = models.ImageField(storage=background_storage, blank=True, null=True)
    mission_statement = models.TextField(default="Our mission is to help the world.")
    about_us_text = models.TextField(default="We are an NGO dedicated to making a difference.")
    contact_phone = models.CharField(max_length=20, default="9120310904")
    contact_email = models.EmailField(default="pankajking67@gmail.com")
    
    is_active = models.BooleanField(default=True, help_text="Set to true to make this the active settings")

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.name} Settings"

class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(storage=gallery_storage)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Volunteer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interests = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Donation(models.Model):
    donor_name = models.CharField(max_length=200)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - ${self.amount}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, help_text="A short bio about the user")
    social_link = models.URLField(blank=True, null=True, help_text="Link to LinkedIn, Twitter, etc.")
    
    # Developer / Admin Specific Details
    role = models.CharField(max_length=200, blank=True, null=True, help_text="e.g. Full-Stack Developer")
    contribution = models.TextField(blank=True, null=True)
    technologies = models.TextField(blank=True, null=True)
    features_developed = models.TextField(blank=True, null=True)
    security_performance = models.TextField(blank=True, null=True)
    purpose_of_project = models.TextField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which this section appears on the About page")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, help_text="Email or Phone Number")
    subject = models.CharField(max_length=200)
    details = models.TextField()
    evidence = models.FileField(upload_to='complaints/', blank=True, null=True, help_text="Upload screenshot or document (optional)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name} ({self.status})"
