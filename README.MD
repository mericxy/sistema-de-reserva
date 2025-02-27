# Sistema de Reserva

Este projeto utiliza Django para gerenciar um sistema de reservas. Ele pode ser executado tanto manualmente quanto via Docker.

## Requisitos

Antes de iniciar, garanta que você tem os seguintes requisitos instalados:
- [Python 3.10](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/) (caso opte pela execução via Docker)

## Executando com Docker (Recomendado)

1. **Construa a imagem do Docker:**
   ```sh
   docker-compose build
   ```

2. **Inicie o container:**
   ```sh
   docker-compose up
   ```

A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

Se precisar parar a execução:
   ```sh
   docker-compose down
   ```

## Executando Manualmente (Sem Docker)

1. **Crie um ambiente virtual:**
   ```sh
   python -m venv venv
   ```

2. **Ative o ambiente virtual:**
   - No Linux/macOS:
     ```sh
     source venv/bin/activate
     ```
   - No Windows:
     ```sh
     venv\Scripts\activate
     ```

3. **Atualize o `pip` e instale as dependências:**
   ```sh
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Execute as migrações do banco de dados:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário para acessar o painel de administração (opcional):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Inicie o servidor:**
   ```sh
   python manage.py runserver
   ```

A aplicação estará rodando em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Notas
- O arquivo `docker-compose.yml` define um serviço `web` que executa a aplicação Django.
- O `DEBUG=True` está ativado por padrão no Docker, então tome cuidado ao subir para produção.
- Caso utilize banco de dados PostgreSQL, MySQL ou outro, adicione as configurações necessárias no `.env` e ajuste o `docker-compose.yml`.
