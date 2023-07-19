import json
import string
import requests
import random
import datetime


def test_post_request_with_binary_data():
    url = "https://demo.facebank.store/api/event/create"
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtLnNlcmdlZXZAbWFnbmF0bWVkaWEuY29tIiwiaWF0IjoxNjg5MDg5MTMwLCJleHAiO" \
            "jE2ODk5NTMxMzB9.amZK_vkxIPS4ZfZ4LoXOcq4zM8huEwJjKg3IhVKC_p9SzyFFT_cQKAX_l4cAUz1Mtb9yiYGLPm0b05JSuCw4WA"
    boundary = b"------WebKitFormBoundaryRifXYEEQCp2MEoTa"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary.decode()}",
        "Authorization": f"Bearer {token}"
    }
    formatted_date = datetime.date.today().strftime("%Y-%m-%d")
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
    body += b'Content-Disposition: form-data; name="logo"; filename="passport.png"\r\n'
    body += b"Content-Type: application/octet-stream\r\n\r\n"
    with open("C:\\Users\\jeezou\\PycharmProjects\\pythonProject\\passport.png", "rb") as file:
        body += file.read() + b"\r\n"
    body += b"--" + boundary + b"--"

    response = requests.post(url, headers=headers, data=body)
    response_data = response.json()

    assert response.status_code == 200, f"Код ошибки: {response.status_code}, Текст ошибки: {response.text}"

    assert response_data['message'] == 'success', 'Событие не создано'
