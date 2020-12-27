FROM python:3.7-stretch

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app


ARG my_arg=hello

ENV test=${my_arg}

CMD ["python", "app.py"]
