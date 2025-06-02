from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ItineraryViewSet, BlogPostViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'itineraries', ItineraryViewSet)
router.register(r'blog-posts', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 