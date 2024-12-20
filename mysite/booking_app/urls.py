from rest_framework import routers
from .views import *
from django.urls import path,include
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register(r'review', ReviewViewSet)
router.register(r'booking', BookingViewSet)

urlpatterns = [
    path('urls/', include(router.urls)),
    path('', HotelListApiView.as_view(), name='hotel_list'),
    path('<int:pk>/', HotelDetailApiView.as_view(), name='hotel_detail'),
    path('rooms/', RoomListApiView.as_view(), name='room_list'),
    path('rooms/<int:pk>', RoomDetailApiView.as_view(), name='room_detail'),
    path('rooms/create/', RoomCreateApiView.as_view(), name='room_create'),
    path('rooms/create/<int:pk>', RoomEditApiView.as_view(), name='room_edit'),
    path('country/', CountryApiView.as_view(), name='country_list'),
    path('country/<int:pk>', CountryDetailApiView.as_view(), name='country_detail'),
    path('user/', UserProfileListApiView.as_view(), name='user_list'),
    path('user/<int:pk>', UserProfileDetailApiView.as_view(), name='user_detail'),
    path('hotel/create/', HotelCreateApiView.as_view(), name='hotel_create'),
    path('hotel/create/<int:pk>', HotelEditApiView.as_view(), name='hotel_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

