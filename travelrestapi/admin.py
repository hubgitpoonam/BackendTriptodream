from django.contrib import admin
from .models import Contact, Itinerary, BlogPost, TourPackage, HotelDetails, ItineraryDetails
from django import forms

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_no', 'start_date', 'end_date', 'travellers_count', 'created_at')
    search_fields = ('name', 'email', 'mobile_no')
    list_filter = ('created_at', 'travellers_count')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

class ItineraryDetailsAdminForm(forms.ModelForm):
    class Meta:
        model = ItineraryDetails
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 15, 'cols': 80, 
                                               'placeholder': '● Begin the journey with a drive towards the confluence of Zanskar.\n● Stop by at the Hall of Fame, located near the Leh Airfield.\n● Move on to explore Gurudwara Pathar Sahib.\n\nUse the bullet point (●) at the beginning of each point to properly format the itinerary.'}),
        }

@admin.register(ItineraryDetails)
class ItineraryDetailsAdmin(admin.ModelAdmin):
    form = ItineraryDetailsAdminForm
    list_display = ('tour_package', 'day_number', 'title', 'created_at')
    list_filter = ('tour_package', 'day_number')
    search_fields = ('title', 'description')
    ordering = ('tour_package', 'day_number')

admin.site.register(TourPackage)
admin.site.register(HotelDetails)

