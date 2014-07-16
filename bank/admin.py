from django.contrib import admin

from .models import Card, Operations




class CardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'is_active', 'rest',)
    search_fields = ('number',)
    
    
    
admin.site.register(Card, CardAdmin)
admin.site.register(Operations)