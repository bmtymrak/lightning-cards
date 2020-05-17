from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Deck, Card

# Create your views here.

class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    fields = ['name']
    template_name = 'deck_create.html'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.object.slug})

class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    context_object_name = 'deck'
    template_name = 'deck_detail.html'

    def get_object(self, *args, **kwargs):
        obj = Deck.objects.all().filter(slug=self.kwargs['slug'], user=self.request.user).get()
        return obj

    #Need list of cards associated with the deck
    def get_context_data(self, *args, **kwargs):
        context = super(DeckDetailView, self).get_context_data(*args, **kwargs)
        context['cards'] = Card.objects.all().filter(deck=self.object, deck__user=self.request.user)
        return context



class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'deck_list.html'

    def get_queryset(self):
        return Deck.objects.all().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs=super().get_context_data(**kwargs)
        kwargs.update({'user':self.request.user})
        return kwargs


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = "deck_delete.html"

    def get_success_url(self):
        return reverse_lazy('deck_list')



class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['front', 'back']
    template_name = 'card_create.html'

    def form_valid(self, form):
        self.obj = form.save()
        # deck = Deck.objects.all().filter(slug=self.kwargs['deck_slug']).get()
        self.obj.deck.set(Deck.objects.all().filter(slug=self.kwargs['deck_slug'], user=self.request.user))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.kwargs['deck_slug']})


    
class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    fields = ['front', 'back']
    template_name = 'card_update.html'

    def get_success_url(self):
        return reverse_lazy('practice_front', kwargs={'username':self.request.user.username, 'deck_slug':self.kwargs['deck_slug'], 'pk':self.object.pk})

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "card_delete.html"

    def get_success_url(self):
        return reverse_lazy('deck_detail', kwargs={'username':self.request.user.username, 'slug':self.kwargs['deck_slug']})



class PracticeViewFront(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'practice_front.html'
    def get_object(self):
        cards = list(Card.objects.all().filter(deck__slug=self.kwargs['deck_slug'], deck__user=self.request.user))
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk == 0:
            current_card = cards[0]
        else:
            current_card = Card.objects.all().get(pk=pk)
        
        current_card_index = cards.index(current_card)
        
        try:
            self.next_pk = cards[current_card_index+1].pk
        except IndexError:
            self.next_pk = 0

        return current_card

    def get_context_data(self, **kwargs):
        kwargs=super().get_context_data(**kwargs)
        kwargs.update({'next_pk':self.next_pk})
        kwargs.update({'user':self.request.user})
        kwargs.update({'deck_slug':self.kwargs['deck_slug']})
        kwargs.update({'deck':Deck.objects.get(slug=self.kwargs['deck_slug'], user=self.request.user)})
        return kwargs


class PracticeViewBack(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'practice_back.html'
    def get_object(self):
        cards = list(Card.objects.all().filter(deck__slug=self.kwargs['deck_slug'], deck__user=self.request.user))
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk == 0:
            current_card = cards[0]
        else:
            current_card = Card.objects.all().get(pk=pk)
        
        current_card_index = cards.index(current_card)
        
        try:
            self.next_pk = cards[current_card_index+1].pk
        except IndexError:
            self.next_pk = 0

        return current_card

    def get_context_data(self, **kwargs):
        kwargs=super().get_context_data(**kwargs)
        kwargs.update({'next_pk':self.next_pk})
        kwargs.update({'user':self.request.user})
        kwargs.update({'deck_slug':self.kwargs['deck_slug']})
        kwargs.update({'deck':Deck.objects.get(slug=self.kwargs['deck_slug'], user=self.request.user)})
        return kwargs
