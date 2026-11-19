import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from .models import ShortLink


@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_redirect_uses_cache(api_client):
    link = ShortLink.objects.create(original_url='https://cached.com', short_code='cache1')
    
    response = api_client.get(f'/{link.short_code}/')
    assert response.status_code == 302
    
    cached_url = cache.get(f"short_link_{link.short_code}")
    assert cached_url == 'https://cached.com'
    
    link.delete()

@pytest.mark.django_db
def test_create_short_link(api_client):
    response = api_client.post('/api/links/', {'original_url': 'https://example.com'})
    assert response.status_code == 201
    data = response.json()
    assert data['original_url'] == 'https://example.com'
    assert 'short_url' in data
    assert ShortLink.objects.count() == 1

@pytest.mark.django_db
def test_redirect(api_client):
    link = ShortLink.objects.create(original_url='https://example.com', short_code='abs123')
    response = api_client.get(f'/{link.short_code}/')
    assert response.status_code == 302
    assert response.url == 'https://example.com'

    link.refresh_from_db()
    assert link.clicks == 1