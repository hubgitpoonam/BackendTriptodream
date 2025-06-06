from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.subject}"
        
    class Meta:
        ordering = ['-created_at']

class Itinerary(models.Model):
    TRAVELLER_CHOICES = [
        ('Solo', 'Solo'),
        ('Couple', 'Couple'),
        ('2-4 People', '2-4 People'),
        ('5-10 People', '5-10 People'),
        ('More than 10 People', 'More than 10 People'),
    ]
    
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    travellers_count = models.CharField(max_length=50, choices=TRAVELLER_CHOICES)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.start_date} to {self.end_date}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Itineraries'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Resize image if it's being uploaded for the first time
        if self.pk is None and self.image:
            self.resize_image()
        
        super().save(*args, **kwargs)
    
    def resize_image(self, target_width=600, target_height=600, quality=90):
        """Resize image to target dimensions while maintaining aspect ratio"""
        if not self.image:
            return
            
        img = Image.open(self.image)
        
        # For better image quality, make the source image larger than needed, then crop
        # This ensures we'll get a high-quality 300x300 image
        
        # Calculate dimensions to maintain aspect ratio while ensuring image is large enough
        width, height = img.size
        
        # Determine which dimension to resize by
        if width > height:
            # Landscape orientation
            new_height = target_height
            new_width = int((width / height) * target_height)
        else:
            # Portrait or square orientation
            new_width = target_width
            new_height = int((height / width) * target_width)
        
        # Resize the image
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize with high-quality resampling
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop to get a centered square image
        if new_width != new_height:
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            img = img.crop((left, top, right, bottom))
        
        # Save the resized image
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality)
        output.seek(0)
        
        # Replace the image field with the resized image
        self.image = InMemoryUploadedFile(
            output,
            'ImageField',
            f"{self.image.name.split('.')[0]}.jpg",
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'




class TourPackage(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    image = models.ImageField(upload_to='tour_images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    


class HotelDetails(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    meal_plan = models.CharField(max_length=100)
    nights = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ItineraryDetails(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Use the bullet point symbol (●) at the beginning of each new point for proper formatting in the frontend.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
    
    class Meta:
        ordering = ['tour_package', 'day_number']
        verbose_name = 'Itinerary Day'
        verbose_name_plural = 'Itinerary Days'

    




