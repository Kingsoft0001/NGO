from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('gallery/', views.gallery, name='gallery'),
    path('donate/', views.donate, name='donate'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('contact/', views.contact, name='contact'),
    path('developer/', views.developer, name='developer'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
]
