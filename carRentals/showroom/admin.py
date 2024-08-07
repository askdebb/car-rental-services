from django.contrib import admin
from showroom.models import Car, CarImage, Reservation

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'price')
    search_fields = ('name', 'make')
    inlines = [CarImageInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # After saving the car instance, set the first image as the thumbnail
        if not obj.images.filter(is_thumbnail=True).exists() and obj.images.exists():
            obj.set_thumbnail(obj.images.first().id)

class CarImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'alt_text', 'car', 'is_thumbnail')
    search_fields = ('alt_text',)
    list_filter = ('car', 'is_thumbnail')

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
