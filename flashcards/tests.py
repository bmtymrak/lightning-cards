from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


from .models import Deck, Card
from .forms import DeckForm, CardForm
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

    def test_deck_delete_view(self):
        data = {
            'name':'test deck 1'
        }
        response = self.client.get(reverse('delete_deck', kwargs={'slug':self.deck.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'deck_delete.html')
        response = self.client.post(reverse('delete_deck', kwargs={'slug':self.deck.slug}), data)
        self.assertEqual(Deck.objects.count(), 0)
        self.assertRedirects(response, reverse('deck_list'))

    def test_deck_create_view(self):
        data = {
            'name':'test deck 2',
        }
        response = self.client.get(reverse('new_deck'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'deck_create.html')
        response = self.client.post(reverse('new_deck'), data)
        self.assertEqual(Deck.objects.count(), 2)
        self.assertRedirects(response, reverse('deck_detail', kwargs={'slug':'test-deck-2'}))

    def test_deck_list_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('deck_list'))
        self.assertRedirects(response, '/accounts/login/?next=/lightning-cards/decks/')

    def test_deck_detail_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('deck_detail', kwargs={'slug':self.deck.slug}))
        self.assertRedirects(response, '/accounts/login/?next=/lightning-cards/decks/test-deck/')

    def test_deck_delete_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('delete_deck', kwargs={'slug':self.deck.slug}))
        self.assertRedirects(response, '/accounts/login/?next=/lightning-cards/decks/test-deck/delete/')

    def test_deck_create_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('new_deck'))
        self.assertRedirects(response, '/accounts/login/?next=/lightning-cards/decks/new-deck/')


class CardViewsTest(TestCase):

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

    def test_card_create_view(self):
        data = {
            'front':'test front 2',
            'back':'test back 2',
            'deck':self.deck,
        }
        response = self.client.get(reverse('new_card',  kwargs={'deck_slug':self.deck.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card_create.html')
        response = self.client.post(reverse('new_card', kwargs={'deck_slug':self.deck.slug}), data)
        self.assertEqual(Card.objects.all().filter(deck=self.deck).count(), 2)
        self.assertRedirects(response, reverse('deck_detail', kwargs={'slug':self.deck.slug}))

    def test_card_update_view(self):
        response = self.client.get(reverse('update_card', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card_update.html')
        response = self.client.post(reverse('update_card', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}), data={'front':'test front updated', 'back':'test back updated'})
        self.assertEqual(Card.objects.all().filter(pk=self.card.pk).get().front, 'test front updated')
        self.assertRedirects(response, reverse('practice_front', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))

    def test_card_delete_view(self):
        response = self.client.get(reverse('delete_card', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'card_delete.html')
        response = self.client.post(reverse('delete_card',  kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertEqual(Card.objects.all().count(), 0)
        self.assertRedirects(response, reverse('deck_detail', kwargs={'slug':self.deck.slug}))

    def test_card_practice_front_view(self):
        response = self.client.get(reverse('practice_front', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test front')
        self.assertTemplateUsed(response, 'practice_front.html')

    def test_card_practice_data_front_view(self):
        response = self.client.get(reverse('practice_front_data', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test front')


    def test_card_practice_data_back_view(self):
        response = self.client.get(reverse('practice_back_data', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk, 'side':'back'}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test back')


    def test_card_create_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('new_card',  kwargs={'deck_slug':self.deck.slug}))
        self.assertRedirects(response, '/accounts/login/?next=/lightning-cards/decks/test-deck/new-card/')

    def test_card_update_view_redirect_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('update_card', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertRedirects(response, f"/accounts/login/?next=/lightning-cards/decks/test-deck/{self.card.pk}/")

    def test_card_delete_view_redirect_not_logged_in(self):
        self.client.logout()
        reponse = self.client.get(reverse('delete_card', kwargs={'deck_slug':self.deck.slug, 'pk':self.card.pk}))
        self.assertRedirects(reponse, f"/accounts/login/?next=/lightning-cards/decks/test-deck/{self.card.pk}/delete/")


class DeckFormTests(TestCase):

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

        
    def test_create_duplicate_deck_not_allowed(self):
        deck_form = DeckForm(data={'name':'test deck', 'user':self.user})
        self.assertFalse(deck_form.is_valid())



class CardFormTests(TestCase):
    
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

    # def test_create_duplicate_card_not_allowed(self):
    #     card_form = CardForm(data={'front':'test front', 'back':'test back', 'deck':self.deck, 'user':self.user})
    #     self.assertFalse(card_form.is_valid())
    #     self.assertFormError(response, card_form, None, 'A card with that name already exists in this deck. Please use a different name')
        