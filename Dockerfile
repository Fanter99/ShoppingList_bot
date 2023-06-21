FROM docker.io/library/python:3.10.6-buster
WORKDIR /app
COPY . .
RUN mkdir /app/data
ENV TELEGRAM_API_TOKEN=###
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]