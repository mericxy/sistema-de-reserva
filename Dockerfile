# Usando uma imagem oficial do Python como base
FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app/

# Atualizar o pip e instalar dependências
RUN pip install --upgrade pip  
RUN pip install -r requirements.txt

# Expor a porta do Django
EXPOSE 8000

# Comando para rodar o servidor do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
