# Use a imagem base do Python
FROM python:3.11-slim

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

EXPOSE 8080

CMD ["functions-framework", "--target=process_event", "--port=8080"]