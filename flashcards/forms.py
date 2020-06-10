from django.forms import ModelForm, ValidationError
from .models import Deck, Card


class DeckForm(ModelForm):

    def clean(self):
        
        cleaned_data = super(DeckForm, self).clean()

        if 'name' in cleaned_data.keys():
            name = cleaned_data['name']
            user = self.data['user']
            
            if Deck.objects.all().filter(name=name, user=user).exists():
                raise ValidationError('A deck with that name already exists. Please use a different name')

    class Meta:
        model=Deck
        fields = ['name']



class CardForm(ModelForm):

    def clean(self):
        
        cleaned_data = super(CardForm, self).clean()

        if 'front' in cleaned_data.keys():
            front = cleaned_data['front']
            deck = self.data['deck']
            
            if Card.objects.all().filter(front=front, deck=deck).exists():
                raise ValidationError('A card with that front already exists in this deck. Please use a different name')

    class Meta:
        model=Card
        fields = ['front', 'back']