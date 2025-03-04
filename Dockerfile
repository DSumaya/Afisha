FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKID /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt


COPY . .
CMD ["nginx", "daemon", "off -g"]