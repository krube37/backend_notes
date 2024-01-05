from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note
from rest_framework.authtoken.models import Token

class NotesAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user1password')
        self.user2 = User.objects.create_user(username='user2', password='user2password')

        self.note1 = Note.objects.create(title='Note 1', content='Content 1', owner=self.user1)
        self.note2 = Note.objects.create(title='Note 2', content='Content 2', owner=self.user1)

        self.client = APIClient()

    def test_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user1password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_create_note(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('note-list'), {'title': 'Note 3', 'content': 'Content 3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_note_list(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # user1 has two notes

    def test_get_note_detail(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('note-detail', kwargs={'pk': self.note1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Note 1')

    def test_update_note(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(reverse('note-detail', kwargs={'pk': self.note1.pk}), {'title': 'Updated Note', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Note')

    def test_delete_note(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('note-detail', kwargs={'pk': self.note1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.filter(pk=self.note1.pk).exists(), False)

    def test_share_note(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('share-note', kwargs={'pk': self.note1.pk}), {'username': 'user2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertIn(self.user2, self.note1.shared_with.all())
