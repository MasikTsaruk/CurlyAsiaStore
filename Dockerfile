FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /gitH

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python","manage.py","runserver"]