import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from .models import Car, Reservation
from .forms import ReservationForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from decouple import config
from decimal import Decimal

FLUTTERWAVE_PUBLIC_KEY = config('FLUTTERWAVE_PUBLIC_KEY')

User = get_user_model()

@login_required
def home_view(request):
    query = request.GET.get('search')
    if query:
        cars = Car.objects.filter(name__icontains=query)
    else:
        cars = Car.objects.all()
    return render(request, 'showroom/sr_home.html', {'cars': cars})

@login_required
def car_details(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    form = ReservationForm()  # Initialize the form here
    return render(request, 'showroom/car_details.html', {'car': car, 'form': form})

@login_required
def make_reservation(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.car = car
            reservation.user = request.user
            reservation.save()

            # Determine sender's email based on reservation type
            sender_email = None
            if reservation.reservation_type == 'individual':
                sender_email = request.user.email  # Use the logged-in user's email for individual reservations
            elif reservation.reservation_type == 'company':
                sender_email = reservation.company_email  # Use the company email for company reservations

            # Send email to the customer
            subject = 'Reservation Confirmation'
            message = 'Your reservation has been confirmed. Your reference number is {}.'.format(reservation.reference_number)
            recipient_list = [request.user.email]

            # Create a tabulated HTML representation of the form data
            html_message = render_to_string('showroom/reservation_email.html', {'reservation': reservation})
            plain_message = strip_tags(html_message)  # Strip HTML tags for the plain text message

            # Send email with both HTML and plain text content
            send_mail(subject, plain_message, sender_email, recipient_list, html_message=html_message)

            # Prepare data for payment initiation with Flutterwave
            tx_ref = f"CAR_RENT_{reservation.reference_number}"
            amount = float(car.price)

            # Prepare payload for Flutterwave Hosted Checkout
            payload = {
                'tx_ref': tx_ref,
                'amount': amount,
                'currency': 'USD',
                'redirect_url': request.build_absolute_uri('/reservation_success/'),
                'payment_options': 'card,mobilemoney,ussd',
                'customer': {
                    'email': request.user.email,
                    'name': request.user.get_full_name()
                },
                'customizations': {
                    'title': 'Car Reservation Payment',
                    'description': 'Payment for car reservation'
                }
            }

            # Make POST request to Flutterwave API to initialize payment
            headers = {
                'Authorization': f'Bearer {FLUTTERWAVE_PUBLIC_KEY}',
                'Content-Type': 'application/json'
            }
            flutterwave_url = 'https://api.flutterwave.com/v3/hosted/pay'
            response = requests.post(flutterwave_url, json=payload, headers=headers)

            if response.status_code == 200:
                # Redirect to Flutterwave checkout page
                data = response.json()
                return redirect(data['data']['link'])
            else:
                # Handle error case, for example:
                error_message = "Failed to initiate payment. Please try again later."
                return render(request, 'showroom/car_details.html', {'car': car, 'form': form, 'error_message': error_message})

        else:
            # Form validation errors
            error_message = "Form validation errors occurred. Please check your inputs."
            return render(request, 'showroom/car_details.html', {'car': car, 'form': form, 'error_message': error_message})

    else:
        # GET request
        form = ReservationForm()

    return render(request, 'showroom/car_details.html', {'car': car, 'form': form})

@login_required
def reservation_success_view(request):
    reservations = Reservation.objects.filter(user=request.user)
    car = get_object_or_404(Car)
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    if status == 'successful':
        # Process successful payment logic here if needed
        return render(request, 'showroom/reservation_success.html', {'tx_ref': tx_ref, 'transaction_id': transaction_id, 'status': status, 'reservations' : reservations, 'car': car })
    else:
        return HttpResponse("Payment was not successful.")
