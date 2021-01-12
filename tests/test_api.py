import os
import requests
from urllib.parse import urljoin
from unittest.mock import Mock, patch

import pytest
from constants import SKIP_REAL, BASE_URL
from app import get_poke_json, get_poke_type_1

BULBA_URL = urljoin(BASE_URL, '1')


@pytest.mark.skipif(SKIP_REAL, reason='Skipping real requests')
def test_request_response():
    response = requests.get(BULBA_URL, verify=False)
    assert response.ok == True


@patch('app.requests.get')
def test_get_poke_json(mock_get):
    mock_get.return_value.ok = True
    response = get_poke_json('charmander')
    assert response.ok == True


@patch('app.requests.get')
def test_get_poke_json_when_response_is_ok(mock_get):
    json_keys = ['abilities', 'base_experience', 'forms', 'game_indices', 'height', 'held_items', 'id', 'is_default',
                 'location_area_encounters', 'moves', 'name', 'order', 'species', 'sprites', 'stats', 'types', 'weight']
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = json_keys

    response = get_poke_json('bulbasaur')

    assert response.json() == json_keys


@patch('app.get_poke_json')
def test_get_poke_type_1(mock_get_poke_json):
    mock_json = {
        'types': [
            {'type':
                 {'name': 'grass'}
             }
        ]
    }

    mock_get_poke_json.return_value = Mock()
    mock_get_poke_json.return_value.json.return_value = mock_json

    type_1 = get_poke_type_1('bulbasaur')

    assert mock_get_poke_json.called
    assert mock_json['types'][0]['type']['name'].capitalize() == type_1

@pytest.mark.skipif(SKIP_REAL, reason='Skipping real requests')
def test_integration_contract():
    '''Checks that the actual shape of the JSON is as expected, that
    it has changed (this code depends upon a third party API).'''
    actual = get_poke_json('bulbasaur')
    actual_keys = list(actual.json().keys())

    with patch('app.requests.get') as mock_get:
        mock_get.ok = True
        mock_get.return_value.json.return_value = {
            'abilities': 1,
            'base_experience': 1,
            'forms': 1,
            'game_indices': 1,
            'height': 1,
            'held_items': 1,
            'id': 1,
            'is_default': 1,
            'location_area_encounters': 1,
            'moves': 1,
            'name': 1,
            'order': 1,
            'species': 1,
            'sprites': 1,
            'stats': 1,
            'types': 1,
            'weight': 1
        }

        mocked = get_poke_json('name')
        mocked_keys = list(mocked.json().keys())

    assert mocked_keys == actual_keys