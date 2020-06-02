from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from .models import Deck, Card
# from users.models import CustomUser
# Create your tests here.


# class FlashcardTest(TestCase):

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             email='testuser@email.com',
#             password='testpass123',
#         )

#         self.deck = Deck.objects.create(
#             name = 'Test Deck'
#         )


class DeckModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'testuser@email.com',
            password = 'testpass123',
        )
        self.deck = Deck.objects.create(name='test deck', user=self.user)

    def test_deck_model_creation(self):
        self.assertEqual(self.deck.name, 'test deck')
        self.assertEqual(self.deck.user, get_user_model().objects.get(username='testuser'))
        self.assertEqual(self.deck.slug, 'test-deck')


class CardModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'testuser@email.com',
            password = 'testpass123',
        )
        self.deck = Deck.objects.create(name='test deck', user=self.user)
        self.card = Card.objects.create(
            front='test front',
            back='test back',
            deck = self.deck)

    def test_card_model_creation(self):
        self.assertEqual(self.card.front, 'test front')
        self.assertEqual(self.card.back, 'test back')
        self.assertEqual(self.card.deck, self.deck)


class DeckViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'testuser@email.com',
            password = 'testpass123',
        )
        self.deck = Deck.objects.create(name='test deck', user=self.user)
        self.client.login(username= self.user.username, password = 'testpass123')
        self.card = Card.objects.create(
            front='test front',
            back='test back',
            deck = self.deck)


    def test_deck_list_view(self):
        response = self.client.get(reverse('deck_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test deck')
        self.assertTemplateUsed(response, 'deck_list.html')


    def test_deck_detail_view(self):
        response = self.client.get(reverse('deck_detail', kwargs={'slug':self.deck.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test front')
        self.assertTemplateUsed(response, 'deck_detail.html')