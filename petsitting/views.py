from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'petsitting/home.html')


def about(request):
    return render(request, 'petsitting/about.html')


def sitters(request):
    return render(request, 'petsitting/sitters.html')


def pets(request):
    return render(request, 'petsitting/pets.html')
