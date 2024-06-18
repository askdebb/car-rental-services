from django.contrib import admin
from .models import Car, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3  # Number of extra inline forms to display

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('name', 'make', 'price')
    list_filter = ('make',)
    search_fields = ('name', 'make')

admin.site.register(Image)
