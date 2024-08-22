# Use a imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o script para o contêiner
COPY main.py main.py

# Comando para executar o script
CMD ["python", "main.py"]