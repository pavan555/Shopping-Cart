from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        #AAA -> Arrange, Act, Assert
        # Arrange any data we need to run the test
        client = APIClient()
        # Act on the code we want to test
        response =client.post('/store/collections/', {"title": "A"})
        # Assert the results are what we expect
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_not_admin_returns_403(self):
        client = APIClient()
        client.force_authenticate(user={})  # Simulating a non-admin user
        response = client.post('/store/collections/', {"title": "A"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_with_invalid_data_returns_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_user_admin_with_valid_data_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {"title": "Amazing Collection"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


    @pytest.mark.skip(reason="Skipping test for demonstration purposes")
    def test_skip_this_test(self):
        print("Skipping test for demonstration purposes")