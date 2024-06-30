# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import home_view, car_details, make_reservation, reservation_success_view

urlpatterns = [
    path('', home_view, name='home'),
    path('showroom/<int:car_id>/', car_details, name='car_details'),
    path('showroom/<int:car_id>/reservation/', make_reservation, name='make_reservation'),
    path('reservation_success/', reservation_success_view, name='reservation_success'),  # Add this URL for reservation success
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
