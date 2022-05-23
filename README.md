# Quiz for exceed team friday parties

Create .env file in root directory of project and set env variables (If you are on frontend you can jut copy and paste vars below)

### .env settings

POSTGRES_DB=example
POSTGRES_USER=example
POSTGRES_PASSWORD=example
POSTGRES_HOST=example
MEDIA_ROOT=media/
SECRET_KEY=secret

If you want up project in containers, you should be use: POSTGRES_HOST=db
If locally: POSTGRES_HOST=localhost:5432

### To accept migrations

- docker exec -ti fojinquiz_web_1 alembic upgrade head

To run project execute <docker-compose up> command

To read API docs please go to <localhost/redoc>

