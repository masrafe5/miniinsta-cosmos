from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Photo, SavedPhoto
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class PhotoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='secret', role='creator')
        self.photo = Photo.objects.create(
            author=self.user,
            title='Sunset',
            caption='Beautiful sunset',
            image=SimpleUploadedFile('sunset.jpg', b'filecontent', content_type='image/jpeg')
        )

    def test_photo_str(self):
        self.assertEqual(str(self.photo), 'Sunset by creator')

    def test_save_photo_unique_constraint(self):
        SavedPhoto.objects.create(photo=self.photo, user=self.user)
        with self.assertRaises(Exception):
            SavedPhoto.objects.create(photo=self.photo, user=self.user)


class PhotoAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='consumer', password='secret', role='consumer')
        self.photo = Photo.objects.create(
            author=User.objects.create_user(username='creator2', password='secret', role='creator'),
            title='Ocean',
            caption='Ocean breeze',
            image=SimpleUploadedFile('ocean.jpg', b'filecontent', content_type='image/jpeg')
        )

    def test_photo_list_api(self):
        response = self.client.get(reverse('api-photo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.json())

    def test_photo_detail_api(self):
        response = self.client.get(reverse('api-photo-detail', kwargs={'pk': self.photo.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Ocean')
