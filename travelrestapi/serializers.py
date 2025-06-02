from rest_framework import serializers
from .models import Contact, Itinerary, BlogPost

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'mobile_no', 'email', 'start_date', 'end_date', 
                 'travellers_count', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 

class BlogPostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'image', 'image_url', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None 