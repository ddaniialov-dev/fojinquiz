# Quiz for exceed team friday parties

Create .env file in root directory of project and set env variables
(If you are on frontend you can jut copy and paste vars below)

### .env settings

### Postgres connection

POSTGRES_DB=example
POSTGRES_USER=example
POSTGRES_PASSWORD=example
POSTGRES_HOST=example

### Web App configs,

MEDIA_ROOT=media/
SECRET_KEY=secret

### PG_Admin settings

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=password

### If you want up project in containers, you should set:

POSTGRES_HOST=db

### If locally:

POSTGRES_HOST=localhost:5432

### If need off CSRF

DEBUG_CSRF=True

### To accept migrations

- docker exec -ti fojinquiz_web_1 alembic upgrade head

### To run project

Execute "docker-compose up" command

### To read API docs

Please go to "http://localhost/redoc/"
