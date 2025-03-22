FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/api
EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "wsgi"]