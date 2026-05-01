from django.urls import path
from . import views

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('add/', views.add_country, name='add_country'),
    path('edit/<str:code>/', views.edit_country, name='edit_country'),
    path('delete/<str:code>/', views.delete_country, name='delete_country'),
    path('report/', views.report, name='report'),
    path('submission-details/', views.submission_details, name='submission_details'),
]