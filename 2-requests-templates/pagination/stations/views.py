import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    file_path = settings.BUS_STATION_CSV
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(reader, 10)
    page = paginator.get_page(page_number)

    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
