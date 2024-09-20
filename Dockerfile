# Use a imagem base do Python
FROM python:3.11-slim

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir o diretório de trabalho
WORKDIR /app

# Comando para rodar o functions-framework e a função main
CMD ["functions-framework", "--target=main"]