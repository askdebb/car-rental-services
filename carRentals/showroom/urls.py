from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import home_view, car_details

urlpatterns = [
    path('', home_view, name='home'),
    path('showroom/<int:car_id>/', car_details, name='car_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
