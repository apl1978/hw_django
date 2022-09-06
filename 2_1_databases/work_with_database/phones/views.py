from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    if sort == 'name':
        phones = Phone.objects.order_by('name').all()
    elif sort == 'min_price':
        phones = Phone.objects.order_by('price').all()
    elif sort == 'max_price':
        phones = Phone.objects.order_by('-price').all()
    else:
        phones = Phone.objects.all()

    context = {'phones':phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug).first()
    context = {'phone':phone}
    return render(request, template, context)
