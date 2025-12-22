from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection, user=None):
        if user is not None:
            api_client.force_authenticate(user=user)
        return api_client.post('/store/collections/', collection)
    return do_create_collection



@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        #AAA -> Arrange, Act, Assert
        # Arrange any data we need to run the test
        # Act on the code we want to test
        response =create_collection({"title": "A"})
        # Assert the results are what we expect
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_not_admin_returns_403(self, create_collection):
        response = create_collection({"title": "A"}, user = {}) # Simulating a non-admin user
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_with_invalid_data_returns_400(self, create_collection):
        response = create_collection({"title": ""}, user = User(is_staff=True))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_user_admin_with_valid_data_returns_201(self, create_collection):
        response = create_collection({"title": "Amazing Collection"}, user = User(is_staff=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


    @pytest.mark.skip(reason="Skipping test for demonstration purposes")
    def test_skip_this_test(self):
        print("Skipping test for demonstration purposes")