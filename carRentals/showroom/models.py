# models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Car(models.Model):
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('CarImage', related_name='cars')

    def __str__(self):
        return self.name

    def set_thumbnail(self, image_id):
        self.images.update(is_thumbnail=False)
        self.images.filter(id=image_id).update(is_thumbnail=True)

class CarImage(models.Model):
    image = models.ImageField(upload_to='car_images/')
    alt_text = models.CharField(max_length=100, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_images', null=True, blank=True)
    is_thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.car.name if self.car else 'Unknown Car'}"

class Reservation(models.Model):
    INDIVIDUAL = 'individual'
    COMPANY = 'company'
    RESERVATION_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    ]

    PENDING = 'pending'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    reservation_type = models.CharField(max_length=10, choices=RESERVATION_TYPE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_contact = models.CharField(max_length=20, blank=True, null=True)
    delivery_method = models.CharField(max_length=10, choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')])
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.reference_number} for {self.car.name} by {self.user.username}"
