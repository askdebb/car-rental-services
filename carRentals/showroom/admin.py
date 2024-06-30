# admin.py
from django.contrib import admin
from .models import Car, CarImage, Reservation

class CarImageInline(admin.TabularInline):
    model = Car.images.through
    extra = 1

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'price')
    search_fields = ('name', 'make')
    inlines = [CarImageInline]

class CarImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'alt_text')
    search_fields = ('alt_text',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'user', 'car', 'reservation_type', 'created_at')
    search_fields = ('reference_number', 'user__username', 'car__name', 'reservation_type')
    list_filter = ('reservation_type', 'delivery_method', 'created_at')
    readonly_fields = ('reference_number', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'car', 'name', 'id_number', 'phone_number', 'address', 'emergency_contact_name', 'emergency_contact_phone', 'reservation_type', 'delivery_method', 'reference_number', 'created_at')
        }),
        ('Company Details', {
            'fields': ('company_name', 'company_email', 'company_contact'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Car, CarAdmin)
admin.site.register(CarImage, CarImageAdmin)
admin.site.register(Reservation, ReservationAdmin)
