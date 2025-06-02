from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Contact, Itinerary, BlogPost
from .serializers import ContactSerializer, ItinerarySerializer, BlogPostSerializer
from django.core.mail import send_mail
from django.conf import settings
import os

# Create your views here.
class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Contact model.
    When a contact is created, it also sends an email notification.
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send email notification
        contact_data = serializer.data
        self.send_contact_email(contact_data)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def send_contact_email(self, contact_data):
        recipient_email = settings.EMAIL_HOST_USER
        subject = f"New Contact Form Submission: {contact_data['subject']}"
        message = f"""
        You have received a new contact form submission:
        
        Name: {contact_data['full_name']}
        Email: {contact_data['email']}
        Subject: {contact_data['subject']}
        Message: {contact_data['message']}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

class ItineraryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Itinerary model.
    When an itinerary is created, it also sends an email notification.
    """
    queryset = Itinerary.objects.all().order_by('-created_at')
    serializer_class = ItinerarySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send email notification
        itinerary_data = serializer.data
        self.send_itinerary_email(itinerary_data)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def send_itinerary_email(self, itinerary_data):
        recipient_email = settings.EMAIL_HOST_USER
        subject = f"New Itinerary Request from {itinerary_data['name']}"
        message = f"""
        You have received a new itinerary request:
        
        Name: {itinerary_data['name']}
        Mobile No: {itinerary_data['mobile_no']}
        Email: {itinerary_data['email']}
        Duration: {itinerary_data['start_date']} to {itinerary_data['end_date']}
        Travellers: {itinerary_data['travellers_count']}
        Comments: {itinerary_data['comments'] if itinerary_data['comments'] else 'No comments provided'}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on BlogPost model.
    """
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context
