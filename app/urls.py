from django.urls import path
from .views import index, services, contacts, reviews, login_view, register_view, cabinet, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('index.html', index, name='index_html'),
    path('services/', services, name='services'),
    path('services.html', services, name='services_html'),
    path('contacts/', contacts, name='contacts'),
    path('contacts.html', contacts, name='contacts_html'),
    path('reviews/', reviews, name='reviews'),
    path('reviews.html', reviews, name='reviews_html'),
    path('cabinet/', cabinet, name='cabinet'),
    path('cabinet.html', cabinet, name='cabinet_html'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
