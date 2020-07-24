from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    ListView,
    DeleteView,
)
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse

import json, random

from .models import Deck, Card
from .forms import DeckForm, CardForm, CardFormSet


class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    form_class = DeckForm
    template_name = "deck_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "POST":
            data = self.request.POST.copy()
            data["user"] = self.request.user
            kwargs["data"] = data

        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("deck_detail", kwargs={"slug": self.object.slug})


class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    context_object_name = "deck"
    template_name = "deck_detail.html"

    def get_object(self, *args, **kwargs):
        obj = (
            Deck.objects.all()
            .filter(slug=self.kwargs["slug"], user=self.request.user)
            .get()
        )
        return obj

    # Need list of cards associated with the deck
    def get_context_data(self, *args, **kwargs):
        context = super(DeckDetailView, self).get_context_data(*args, **kwargs)
        context["cards"] = Card.objects.all().filter(
            deck=self.object, deck__user=self.request.user
        )
        return context


class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = "deck_list.html"

    def get_queryset(self):
        return Deck.objects.all().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({"user": self.request.user})
        return kwargs


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = "deck_delete.html"

    def get_queryset(self):
        return Deck.objects.all().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("deck_list")


# class CardCreateView(LoginRequiredMixin, CreateView):
#     form_class = CardForm
#     template_name = "card_create.html"

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
        
#         if self.request.method == "POST":
#             data = self.request.POST.copy()
#             data["deck"] = (
#                 Deck.objects.all()
#                 .filter(slug=self.kwargs["deck_slug"], user=self.request.user)
#                 .get()
#             )
#             kwargs["data"] = data

#         return kwargs

#     def form_valid(self, form):
#         self.obj = form.save(commit=False)
#         self.obj.deck = (
#             Deck.objects.all()
#             .filter(slug=self.kwargs["deck_slug"], user=self.request.user)
#             .get()
#         )
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("deck_detail", kwargs={"slug": self.kwargs["deck_slug"]})


# class CardCreateView(LoginRequiredMixin, CreateView):
#     # form_class = CardForm
#     form_class = CardFormSet
#     template_name = "card_create.html"

#     # def get_context_data(self, **kwargs):
#     #     data = super(CardCreateView, self).get_context_data(**kwargs)
#     #     # data['formset'] = CardFormSet(queryset=Card.objects.none())

#     #     return data

#     def form_valid(self, form):
#         self.obj = form.save(commit=False)
#         self.obj.deck = (
#             Deck.objects.all()
#             .filter(slug=self.kwargs["deck_slug"], user=self.request.user)
#             .get()
#         )

#         # formset = CardFormSet(data=request.POST)
        
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("deck_detail", kwargs={"slug": self.kwargs["deck_slug"]})

class CardCreateView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "card_create.html"

    def get(self, request, *args, **kwargs):
        formset = CardFormSet(queryset=Card.objects.none())
        return self.render_to_response({'formset':formset})

    def post(self, request, *args, **kwargs):
        formset = CardFormSet(data=request.POST)
        if formset.is_valid():
            
            forms = formset.save(commit=False)
            for form in forms:
                form.deck = Deck.objects.all().filter(slug=self.kwargs["deck_slug"], user=self.request.user).get()
                print(form)
                form.save()
            return redirect(reverse_lazy("deck_detail", kwargs={"slug":self.kwargs["deck_slug"]}))

        return self.render_to_response({'formset':formset})




class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    fields = ["front", "back"]
    template_name = "card_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "practice_front",
            kwargs={"deck_slug": self.kwargs["deck_slug"], "pk": self.object.pk},
        )


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "card_delete.html"

    def get_success_url(self):
        return reverse_lazy("deck_detail", kwargs={"slug": self.kwargs["deck_slug"]})


class PracticeViewFront(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "practice_front.html"

    def get_object(self):
        self.request.session['review_type'] = 'regular'
        self.cards = list(
            Card.objects.all().filter(
                deck__slug=self.kwargs["deck_slug"], deck__user=self.request.user
            )
        )
        self.pk = self.kwargs.get(self.pk_url_kwarg)

        current_card = Card.objects.all().get(pk=self.pk)

        current_card_index = self.cards.index(current_card)

        try:
            self.next_pk = self.cards[current_card_index + 1].pk
        except IndexError:
            self.next_pk = self.cards[0].pk

        return current_card

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({"next_pk": self.next_pk})
        kwargs.update({"deck_slug": self.kwargs["deck_slug"]})
        kwargs.update({"deck": Deck.objects.get(slug=self.kwargs["deck_slug"], user=self.request.user)})
        kwargs.update({"cards": self.cards})
        return kwargs


class PracticeDataFront(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "practice_front.html"

    def get_object(self):
        self.cards = list(Card.objects.all().filter(deck__slug=self.kwargs["deck_slug"], deck__user=self.request.user))
        self.pk = self.kwargs.get(self.pk_url_kwarg)

        current_card = Card.objects.all().get(pk=self.pk)

        current_card_index = self.cards.index(current_card)

        try:
            self.next_pk = self.cards[current_card_index + 1].pk
        except IndexError:
            self.next_pk = self.cards[0].pk

        return current_card

    def render_to_response(self, context, **response_kwargs):

        if self.request.is_ajax():
            data = {
                "text": context["object"].front,
                "side": "back",
                "deck": self.kwargs["deck_slug"],
                "card_pk": self.pk,
                "next_pk": self.next_pk,
            }
            return JsonResponse(data)

        else:
            return super().render_to_response(context)


@login_required
def PracticeDataBack(request, deck_slug, pk, side):
    submitted_card = Card.objects.all().get(deck__user = request.user, deck__slug=deck_slug, pk=pk)

    if side == 'front':
        text = submitted_card.front
        new_side = 'back'
        
    elif side == 'back':
        text = submitted_card.back
        new_side = 'front'
        

    data = {
        'text':text,
        'deck':deck_slug,
        'card_pk':submitted_card.pk,
        'side': new_side
    }

    if request.is_ajax():
        return JsonResponse(data)

class PracticeViewFrontRanking(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "practice_front.html"

    def get_object(self):
        self.cards = list(Card.objects.all().filter(deck__slug=self.kwargs["deck_slug"], deck__user=self.request.user).order_by("proficiency"))
        self.request.session['review_order'] = [card.pk for card in self.cards]
        self.request.session['review_type'] = 'ranked'
        self.pk = self.kwargs.get(self.pk_url_kwarg)

        current_card = self.cards[0]

        current_card_index = self.cards.index(current_card)

        try:
            self.next_pk = self.cards[current_card_index + 1].pk
        except IndexError:
            self.next_pk = self.cards[0].pk

        return current_card

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({"next_pk": self.next_pk})
        kwargs.update({"deck_slug": self.kwargs["deck_slug"]})
        kwargs.update({"deck": Deck.objects.get(slug=self.kwargs["deck_slug"], user=self.request.user)})
        kwargs.update({"cards": self.cards})
        return kwargs


@login_required
def PracticeDataFrontRanking(request, deck_slug, pk):

    print(request.content_type)
    #Get data from AJAX POST
    difficulty = json.loads(request.body)['difficulty']
    card_front = json.loads(request.body)['card']

    submitted_card = Card.objects.all().get(deck__user = request.user, deck__slug=deck_slug, front=card_front)
    submitted_card.update_proficiency(difficulty)

    review_order = request.session.get('review_order', [])
    cards = list(Card.objects.all().filter(deck__slug=deck_slug, deck__user=request.user).order_by('proficiency'))

    #If the last reviewed card is still the lowest ranked card, insert
    #it randomly into the top half of the deck. Otherwise, add it to the end
    if cards[0] == submitted_card:
        swap_index = random.randint(1, len(cards)/2)
        first_card = review_order.pop(0)
        review_order.insert(swap_index, first_card)

    else:
        review_order.append(review_order.pop(0))
    
    pk = review_order[0]
    
    current_card = Card.objects.get(deck__user=request.user, pk=pk)
    next_pk = review_order[1]

    request.session['review_order'] = review_order

    if request.is_ajax():
        data = {
            "text": current_card.front,
            "side": "back",
            "deck": deck_slug,
            "card_pk": pk,
            "next_pk": next_pk,
        }
        return JsonResponse(data)
