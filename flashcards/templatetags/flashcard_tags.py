from django import template
from ..models import Deck


register = template.Library()


@register.inclusion_tag('users_decks.html', takes_context=True)
def display_users_decks(context):
    users_decks = Deck.objects.all().filter(user=context['request'].user)
    return {'users_decks': users_decks}
