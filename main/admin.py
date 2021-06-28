from django.contrib import admin
from .models import Shortener

@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_url', 'short_url')

