# Production Docker Image
FROM docker.io/library/python:3.7-stretch

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]
