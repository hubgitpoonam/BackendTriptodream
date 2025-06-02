from django.contrib import admin
from .models import Contact, Itinerary, BlogPost

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
