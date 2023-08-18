FROM python:3.9

LABEL maintainer="Paulo Mota"

RUN pip install fastapi uvicorn gunicorn

COPY . .

RUN  pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

