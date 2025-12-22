from rest_framework import status
from rest_framework.test import APIClient
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
    
    @pytest.mark.skip(reason="Skipping test for demonstration purposes")
    def test_skip_this_test(self):
        pytest.skip("Skipping test for demonstration purposes")