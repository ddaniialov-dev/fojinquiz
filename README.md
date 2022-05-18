# Quiz for exceed team friday parties

Create .env file in root directory of project and set env variables (If you are on frontend you can jut copy and paste vars below)

### .env settings

POSTGRES_DB=example
POSTGRES_USER=example
POSTGRES_PASSWORD=example
POSTGRES_HOST=example
MEDIA_ROOT=/media/
SECRET_KEY=secret

### To accept migrations

- docker exec -ti fojinquiz-web-1 alembic upgrade head

To run project execute <docker-compose up> command

To read API docs please go to <localhost/redoc>
