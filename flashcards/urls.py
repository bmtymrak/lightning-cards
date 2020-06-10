from django.urls import path

from .views import DeckCreateView, DeckDetailView, CardCreateView, CardUpdateView, DeckListView, DeckDeleteView, CardDeleteView, PracticeViewFront, PracticeDataFront, PracticeDataBack



urlpatterns = [
    path('decks/new-deck/', DeckCreateView.as_view(), name="new_deck"),
    path('decks/<slug:slug>/', DeckDetailView.as_view(), name="deck_detail"),
    path('decks/<slug:deck_slug>/new-card/', CardCreateView.as_view(), name="new_card"),
    path('decks/<slug:deck_slug>/<int:pk>/', CardUpdateView.as_view(), name="update_card"),
    path('decks/<slug:slug>/delete/', DeckDeleteView.as_view(), name="delete_deck"),
    path('decks/<slug:deck_slug>/<int:pk>/delete/', CardDeleteView.as_view(), name="delete_card"),
    path('decks/<slug:deck_slug>/practice/<int:pk>/front/', PracticeViewFront.as_view(), name="practice_front" ),
    path('decks/<slug:deck_slug>/<int:pk>/front/', PracticeDataFront.as_view(), name="practice_front_data" ),
    path('decks/<slug:deck_slug>/<int:pk>/back/', PracticeDataBack.as_view(), name="practice_back_data" ),
    path('decks/', DeckListView.as_view(), name="deck_list"),
]