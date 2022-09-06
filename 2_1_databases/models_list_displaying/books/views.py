from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books':books}
    return render(request, template, context)

def books_pub_date_view(request, pub_date):
    template = 'books/books_pub_date.html'
    books = Book.objects.filter(pub_date=pub_date).all()

    dates = Book.objects.order_by('pub_date').distinct('pub_date').values('pub_date')
    paginator = Paginator(dates, 1)

    page_number = 1
    for page in paginator:
        if str(page[0]['pub_date']) == pub_date:
            page_number = page.number
            break
    page = paginator.get_page(page_number)
    previous = paginator.get_page(page_number - 1)
    next = paginator.get_page(page_number + 1)

    context = {
        'books': books,
        'page': page,
        'previous_date': str(previous[0]['pub_date']),
        'next_date': str(next[0]['pub_date'])
    }
    return render(request, template, context)
