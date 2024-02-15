import email
from accounts.models import *
from rest_framework.test import APITestCase 
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
# testcase

class UserProfileTest( APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            "first_name": "test",
            "last_name": "test",
            'gender': 'male'
        }
        self.profile_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'This is a test bio.',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
        }

        # Create a user and obtain a token for authentication
        url=reverse('rest_register')
        self.client.post(url, self.user_data, format='json')

        self.user = User.objects.get(email=self.user_data['email'])
        # self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        # profile_id=self.user.profile.id
        # print("hhh")
        # print(profile_id)
        # Set the Authorization header with the token
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

 

    def test_update_user_profile_without_token(self):
        # pass
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id
        response = self.client.put(url, self.profile_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def teste_update_user_profile_with_invalid_token(self):
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}invalid')
        response = self.client.put(url, self.profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        # requied token for update profile
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id

        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.put(url, self.profile_data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_update_user_profile_without_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.id+1000])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, self.profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_update_user_profile_without_user(self):
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id+1000
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, self.profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_delete_user_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_get_user_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.id])  # Assuming 'profile-detail' is the name generated by the router
        self.profile_data['user'] = self.user.id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_user_profiles (self):
        url = reverse('profile-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filters_by_user_id(self):
        url = reverse('rest_register')
        for i in range(30):
            data={
                'email': f'test{i}@test.com',
                'username': f'test{i}',
                'password': 'testpassword',
                'first_name': 'test',
                'last_name': 'test',
                'date_of_birth': '1990-01-01',
                'gender': 'Male',
            }
            self.client.post(url, self.user_data, format='json')


        url = '/accounts/profile/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url , {'user__id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response = self.client.get(url , {'user__id': '10100'})
        self.assertEqual(len(response.data), 0)        