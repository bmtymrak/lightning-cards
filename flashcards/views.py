from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse, reverse_lazy

from .models import Deck, Card

# Create your views here.

class DeckCreateView(CreateView):
    model = Deck
    fields = ['name']
    template_name = 'deck_create.html'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.object.slug})

class DeckDetailView(DetailView):
    model = Deck
    context_object_name = 'deck'
    template_name = 'deck_detail.html'

    #Need list of cards associated with the deck
    def get_context_data(self, *args, **kwargs):
        context = super(DeckDetailView, self).get_context_data(*args, **kwargs)
        context['cards'] = Card.objects.all().filter(deck=self.object)
        return context



class DeckListView(ListView):
    model = Deck
    template_name = 'deck_list.html'

    def get_queryset(self):
        return Deck.objects.all().filter(user=self.request.user)




class CardCreateView(CreateView):
    model = Card
    fields = ['front', 'back']
    template_name = 'card_create.html'

    def form_valid(self, form):
        self.obj = form.save()
        deck = Deck.objects.all().filter(slug=self.kwargs['deck_slug']).get()
        self.obj.deck.set(Deck.objects.all().filter(slug=self.kwargs['deck_slug']))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.kwargs['deck_slug']})


    
class CardUpdateView(UpdateView):
    model = Card
    fields = ['front', 'back']
    template_name = 'card_update.html'

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.deck.slug})