from django.contrib import admin
from .models import Deck, Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'deck', 'proficiency')
    list_filter = ('deck',)

admin.site.register(Deck)
# admin.site.register(Card)