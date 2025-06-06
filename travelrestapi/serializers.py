from rest_framework import serializers
from .models import Contact, Itinerary, BlogPost, TourPackage, HotelDetails, ItineraryDetails

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
    

class HotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelDetails
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ItineraryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryDetails
        fields = ['id', 'tour_package', 'day_number', 'title', 'description', 'created_at', 'updated_at']

class ItineraryDaySerializers(serializers.ModelSerializer):
    class Meta:
        model = ItineraryDetails
        fields = ['id', 'day_number', 'title', 'description']

class TourPackageSerializer(serializers.ModelSerializer):
    hotels = serializers.SerializerMethodField()
    itinerary = serializers.SerializerMethodField()

    class Meta:
        model = TourPackage
        fields = ['id', 'title', 'duration', 'image', 'description', 'hotels', 'itinerary']

    def get_hotels(self, obj):
        hotels = HotelDetails.objects.filter(tour_package=obj)
        return HotelDetailsSerializer(hotels, many=True).data

    def get_itinerary(self, obj):
        itinerary = ItineraryDetails.objects.filter(tour_package=obj).order_by('day_number')
        return ItineraryDetailsSerializer(itinerary, many=True).data