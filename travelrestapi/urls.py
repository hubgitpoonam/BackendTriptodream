from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ItineraryViewSet, BlogPostViewSet, TourPackageViewSet, HotelDetailViewSet, ItineraryDayViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'itineraries', ItineraryViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'tour-packages', TourPackageViewSet)
router.register(r'hotel-details', HotelDetailViewSet)
router.register(r'itinerary-days', ItineraryDayViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 