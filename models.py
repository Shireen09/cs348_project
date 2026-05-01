from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    population = models.IntegerField()
    capital = models.ForeignKey(
    'City',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='capital_countries'
    )

    class Meta:
        indexes = [
            # Supports report filters by continent and ordered country listings.
            models.Index(fields=['continent', 'name'], name='country_cont_name_idx'),
        ]

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    population = models.IntegerField()

    def __str__(self):
        return self.name


class CountryLanguage(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    is_official = models.BooleanField()
    percentage = models.FloatField()

    class Meta:
        indexes = [
            # Supports report filters by language and country-language joins.
            models.Index(fields=['language', 'country'], name='lang_country_idx'),
        ]

    def __str__(self):
        return f"{self.language} ({self.country.code})"