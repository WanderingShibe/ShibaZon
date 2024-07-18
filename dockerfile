FROM python:3.9-slim

WORKDIR /ShibaZon

COPY . /ShibaZon
# COPY requirements.txt .
# COPY app.py .

RUN pip install -r requirements.txt

EXPOSE 5050 5432

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]