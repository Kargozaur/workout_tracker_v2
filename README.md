uv run alembic -c app/workout/alembic.ini revision --autogenerate -m "initial migration"
uv run alembic -c app/workout/alembic.ini upgrade head