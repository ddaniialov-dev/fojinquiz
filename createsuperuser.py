import typer
from sqlalchemy import create_engine, insert

from quiz_project.conf import Settings
from quiz_project.utils.functions import hash_password
from user_app.models import User

cli = typer.Typer()


@cli.command()
def createsuperuser(
        username: str, email: str, password: str
):
    engine = create_engine(Settings.DATABASE_SYNC_URL, future=True)
    with engine.begin() as connection:
        password = hash_password(username, password)
        query = (
            insert(User).
            values(
                username=username,
                hashed_password=password,
                email=email,
                is_admin=True
            )
        )
        connection.execute(query)


if __name__ == '__main__':
    cli()
