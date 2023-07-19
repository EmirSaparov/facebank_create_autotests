FROM python:3.9

WORKDIR ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "test_facebank.py"]