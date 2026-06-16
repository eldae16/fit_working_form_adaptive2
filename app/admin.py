from django.contrib import admin
from .models import Request, Review

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'car', 'service', 'created_at')
    search_fields = ('name', 'phone', 'car', 'service')
    list_filter = ('created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'car', 'rating', 'created_at')
    search_fields = ('name', 'car', 'text')
    list_filter = ('rating', 'created_at')
