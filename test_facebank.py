import json
import string
import requests
import random
import datetime
import os


class TestEventAPITestCase:
    base_url = "https://demo.facebank.store/api/"
    event_id = "47"
    album_id = "78"
    photo_id = "2783"
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtLnNlcmdlZXZAbWFnbmF0bWVkaWEuY29tIiwiaWF0IjoxNjg5MDg5MTMwLCJle" \
            "HAiOjE2ODk5NTMxMzB9.amZK_vkxIPS4ZfZ4LoXOcq4zM8huEwJjKg3IhVKC_p9SzyFFT_cQKAX_l4cAUz1Mtb9yiYGLPm0b05JSuCw4WA"
    directory_path = os.path.dirname(os.path.realpath(__file__))

    def test_post_create_event(self):
        boundary = b"------WebKitFormBoundaryRifXYEEQCp2MEoTa"
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary.decode()}",
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            "nameRu": ''.join(random.choices(string.ascii_letters, k=10)),
            "nameEn": ''.join(random.choices(string.ascii_letters, k=10)),
            "startDate": formatted_date,
            "endDate": formatted_date,
            "coords": "55.755864,37.617698"
        }

        body = b""
        body += b"--" + boundary + b"\r\n"
        body += b'Content-Disposition: form-data; name="info"\r\n'
        body += b"Content-Type: application/json\r\n\r\n"
        body += json.dumps(data).encode('utf-8') + b"\r\n"

        body += b"--" + boundary + b"\r\n"
        body += b'Content-Disposition: form-data; name="logo"; filename="logo.png"\r\n'
        body += b"Content-Type: application/octet-stream\r\n\r\n"
        with open(f"{self.directory_path}\\logo.png", "rb") as file:
            body += file.read() + b"\r\n"
        body += b"--" + boundary + b"--"

        response = requests.post(url=f"{self.base_url}event/create", headers=headers, data=body)
        response_data = response.json()
        # self.event_id = response_data['id']
        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"
        assert response_data['message'] == 'success', 'Событие не создано'
        assert self.event_id is not None, 'ID события не существует'

    def test_post_create_album(self):
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        data = {
            "nameRu": "1122",
            "nameEn": "1122",
            "datetime": formatted_date,
            "eventId": self.event_id,
            "categories": [],
            "defaultPrice": 0
        }

        response = requests.post(url=f"{self.base_url}album/create", headers=headers, json=data)
        # response_data = response.json()

        # self.album_id = response_data['id']
        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"
        assert self.album_id is not None, 'ID события не существует'

    def test_post_add_photo(self):
        boundary = "----WebKitFormBoundarylBQfJwNAjftLONz5"
        key = "ca3ef647ef22889b54a7d23d7f102165121b36809976427fe2e826e298bdd6ac"

        headers = {
            # "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {self.token}"
        }

        files = [
            ("file", ('test_photo.jpg', open(f"{self.directory_path}\\test_photo.jpg", "rb"), "image/jpeg")),
            ('info', ('test_json.json', open(f"{self.directory_path}\\test_json.json", "rb"), "application/json"))
        ]

        data = {
            'albumId': self.album_id,
            'key': key
        }

        response = requests.post(url=f"{self.base_url}s3/upload-once", headers=headers, data=data, files=files)
        response_data = response.json()
        self.photo_id = response_data['id']
        assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"

    def test_get_photo_id(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=f"{self.base_url}photos/{self.photo_id}/info", headers=headers)

        assert '2783' in response.text, "Photo id doesn't match"
