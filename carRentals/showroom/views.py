from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car

# Create your views here.
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
    return render(request, 'showroom/car_details.html', {'car': car})
