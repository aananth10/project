import json
import pytest
from backend.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_realtime_latest_all(client):
    response = client.get('/api/realtime/latest')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert isinstance(data['data'], dict)


def test_realtime_latest_city_missing(client):
    response = client.get('/api/realtime/latest?city=CityDoesNotExistXYZ')
    # for missing city may still return {} success or 404, normalize
    assert response.status_code in (200, 404)


def test_city_area_timeline_missing_city(client):
    response = client.get('/api/city/CityDoesNotExistXYZ/area/None/timeline')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'


def test_city_area_timeline_valid_format(client):
    # choose first known city and area from data_generator with available persisted file output
    # if persisted file not available in CI, this is skipped gracefully.
    example_city = 'Mumbai'
    example_area = 'South Mumbai'
    response = client.get(f'/api/city/{example_city}/area/{example_area}/timeline')

    if response.status_code == 404:
        pytest.skip("No persisted data available for timeline endpoint")

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['city'] == example_city
    assert data['area'] == example_area
    assert 'timeline_30day' in data
    assert len(data['timeline_30day']) == 30
    for point in data['timeline_30day']:
        assert 'date' in point
        assert 'risk_level' in point
        assert 'rainfall_mm' in point
