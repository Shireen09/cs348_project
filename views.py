from django.db import connection, transaction
from django.shortcuts import get_object_or_404, render, redirect
from .models import Country, CountryLanguage
from .forms import CountryForm


def _set_repeatable_read_if_supported():
    """
    Demonstrates explicit isolation-level selection for backends that support it.
    SQLite ignores this setting, while PostgreSQL/MySQL support it.
    """
    if connection.vendor in {"postgresql", "mysql"}:
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")


# List all countries
def country_list(request):
    countries = Country.objects.all().order_by('name')
    return render(request, 'country_list.html', {'countries': countries})


# Add country
def add_country(request):
    form = CountryForm(request.POST or None)
    if form.is_valid():
        with transaction.atomic(): # ensures atomicity
            _set_repeatable_read_if_supported() # RR
            form.save() # save form
        return redirect('country_list')
    return render(request, 'form.html', {'form': form})


# Edit country
def edit_country(request, code):
    country = get_object_or_404(Country, code=code)
    form = CountryForm(request.POST or None, instance=country)
    if form.is_valid():
        with transaction.atomic(): # ensures atomicity
            _set_repeatable_read_if_supported() # RR
            # Lock row for concurrent edits when backend supports row locking.
            Country.objects.select_for_update().filter(code=code).first() # filter
            form.save() # save form
        return redirect('country_list')
    return render(request, 'form.html', {'form': form})


# Delete country
def delete_country(request, code):
    with transaction.atomic():
        _set_repeatable_read_if_supported()
        country = get_object_or_404(Country.objects.select_for_update(), code=code) # get object or 404
        country.delete()
    return redirect('country_list')


# Report page
def report(request):
    continent = request.GET.get('continent')
    language = request.GET.get('language')

    countries = Country.objects.all().order_by('name')

    if continent:
        countries = countries.filter(continent=continent)

    if language:
        countries = countries.filter(countrylanguage__language=language).distinct()

    continents = Country.objects.values_list('continent', flat=True).distinct()
    languages = CountryLanguage.objects.values_list('language', flat=True).distinct()

    return render(request, 'report.html', {
        'countries': countries,
        'continents': continents,
        'languages': languages
    })


def submission_details(request):
    return render(request, "submission_details.html")