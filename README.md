uv run alembic -c app/workout/alembic.ini revision --autogenerate -m "initial migration"

uv run alembic -c app/workout/alembic.ini upgrade head

celery -A app.workout.infrastructure.tasks.celery_client worker --beat -l info