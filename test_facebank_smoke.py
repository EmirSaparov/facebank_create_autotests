import requests


class TestUserFacebank:

    base_url = "https://facebank.store/"

    def test_page_opens(self):
        response = requests.get(url=self.base_url)
        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"

    def test_search_by_text(self):
        response = requests.get(f'{self.base_url}api/search?query=%D1%84%D0%BE%D1%80%D1%83%D0%BC')
        response_data = response.json()
        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"
        assert len(response_data['photos']) == 41, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"

    def test_search_by_face(self):
        with open('emir_test_photo.png', 'rb') as file:
            photo_data = file.read()

        boundaries = b'----WebKitFormBoundary4he959pEG3a4RSo7'
        headers = {'Content-Type': f'multipart/form-data; boundary={boundaries.decode()}'}
        data = b''
        data += b'--' + boundaries + b'\r\nContent-Disposition: form-data; name="photo"; ' \
                                     b'filename="emir_test_photo.png"\r\n' \
                                     b'Content-Type: image/png\r\n\r\n'
        data += photo_data
        data += b'\r\n--' + boundaries + b'--\r\n'

        response = requests.post(url=f'{self.base_url}api/search', headers=headers, data=data)

        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"
