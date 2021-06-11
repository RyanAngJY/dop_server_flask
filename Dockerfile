# Production Docker Image
FROM docker.io/library/python:3.7-stretch

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

RUN apt-get update && apt-get install make jq -y
RUN make install_gen

CMD ["python", "app.py"]
