FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install gunicorn
RUN pip install setuptools 
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /app/
