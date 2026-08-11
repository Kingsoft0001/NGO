from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import SiteSettings, Campaign, GalleryImage, Volunteer, Donation, ContactMessage, UserProfile, AboutSection, Story, Complaint

def get_site_settings():
    settings = SiteSettings.objects.filter(is_active=True).first()
    if not settings:
        settings = SiteSettings.objects.first()
    return settings

def home(request):
    if request.method == 'POST' and 'complaint_submit' in request.POST:
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        subject = request.POST.get('subject')
        details = request.POST.get('details')
        evidence = request.FILES.get('evidence')
        
        if name and contact and subject and details:
            Complaint.objects.create(
                name=name,
                contact=contact,
                subject=subject,
                details=details,
                evidence=evidence
            )
            messages.success(request, "Your complaint has been submitted successfully. We will review it shortly.")
            return redirect('home')
        else:
            messages.error(request, "Please fill in all required fields.")

    settings = get_site_settings()
    campaigns = Campaign.objects.filter(is_active=True).order_by('-created_at')[:3]
    stories = Story.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'settings': settings, 
        'campaigns': campaigns,
        'stories': stories
    })

def about(request):
    settings = get_site_settings()
    about_sections = AboutSection.objects.filter(is_active=True)
    return render(request, 'about.html', {
        'settings': settings,
        'about_sections': about_sections
    })

def campaigns(request):
    settings = get_site_settings()
    campaigns = Campaign.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'campaigns.html', {'settings': settings, 'campaigns': campaigns})

def gallery(request):
    settings = get_site_settings()
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery.html', {'settings': settings, 'images': images})

def donate(request):
    settings = get_site_settings()
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        campaign_id = request.POST.get('campaign_id')
        message = request.POST.get('message')

        campaign = None
        if campaign_id:
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.raised_amount += float(amount)
            campaign.save()

        Donation.objects.create(
            donor_name=donor_name,
            email=email,
            amount=amount,
            campaign=campaign,
            message=message
        )
        messages.success(request, 'Thank you for your generous donation!')
        return redirect('donate')

    campaigns = Campaign.objects.filter(is_active=True)
    return render(request, 'donate.html', {'settings': settings, 'campaigns': campaigns})

def volunteer(request):
    settings = get_site_settings()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        interests = request.POST.get('interests')

        Volunteer.objects.create(
            name=name,
            email=email,
            phone=phone,
            interests=interests
        )
        messages.success(request, 'Thank you for registering as a volunteer!')
        return redirect('volunteer')
    
    return render(request, 'volunteer.html', {'settings': settings})

def contact(request):
    settings = get_site_settings()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html', {'settings': settings})

def developer(request):
    settings = get_site_settings()
    # Fetch the developer profile (assuming it's the first superuser or named 'pankaj')
    developer_user = User.objects.filter(is_superuser=True).first()
    developer_profile = None
    if developer_user and hasattr(developer_user, 'profile'):
        developer_profile = developer_user.profile
    
    return render(request, 'developer.html', {
        'settings': settings, 
        'profile': developer_profile,
        'developer_name': f"{developer_user.first_name} {developer_user.last_name}".strip() if developer_user and (developer_user.first_name or developer_user.last_name) else (developer_user.username if developer_user else "Er Pankaj Kumar Yadav")
    })

from django.shortcuts import get_object_or_404

def story_detail(request, story_id):
    settings = get_site_settings()
    story = get_object_or_404(Story, id=story_id, is_active=True)
    return render(request, 'story_detail.html', {
        'settings': settings,
        'story': story
    })
