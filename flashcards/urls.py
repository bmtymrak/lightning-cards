from django.urls import path

from .views import DeckCreateView, DeckDetailView, CardCreateView, CardUpdateView, DeckListView



urlpatterns = [
    path('new-deck/', DeckCreateView.as_view(), name="new_deck"),
    path('<str:username>/<slug:slug>/', DeckDetailView.as_view(), name="deck_detail"),
    path('<str:username>/<slug:deck_slug>/new-card/', CardCreateView.as_view(), name="new_card"),
    path('<str:username>/<slug:deck_slug>/<int:pk>/', CardUpdateView.as_view(), name="update_card"),
    path('decks/', DeckListView.as_view(), name="deck_list")
]