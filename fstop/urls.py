from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet
from .views import ProjectViewSet
from .views import BookingViewSet
from .views import GalleryViewSet
from .views import UserSignupView

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'galleries', GalleryViewSet, basename='gallery')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/signup/', UserSignupView.as_view(), name='signup'),
]
