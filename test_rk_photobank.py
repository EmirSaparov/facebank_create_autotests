import requests


class TestRKPhotobank:
    base_url = 'https://photo.roscongress.org/ru/'

    def test_page_opens(self):
        response = requests.get(f'{self.base_url}')
        assert response.status_code == 200, f'Fail status-code: {response.status_code}, Fail text: {response.text}'

    def test_search_by_text(self):
        response = requests.get(f'{self.base_url}/api/structure/search&query=%D1%84%D0%BE%D1%80%')
        assert response.status_code == 200, f'Fail status-code: {response.status_code}, Fail text: {response.text}'