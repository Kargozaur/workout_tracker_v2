from fastapi import APIRouter

from app.workout.presentation.api.v1.auth import create_auth_router
from app.workout.presentation.api.v1.exercises import create_exercise_router
from app.workout.presentation.api.v1.items import create_items_router
from app.workout.presentation.api.v1.user import create_user_router
from app.workout.presentation.api.v1.workout import create_workout_router


def create_api_router() -> APIRouter:
    api_router = APIRouter(prefix="/api")
    v1_router = APIRouter(prefix="/v1", tags=["v1"])
    v1_router.include_router(create_auth_router())
    v1_router.include_router(create_user_router())
    v1_router.include_router(create_exercise_router())
    v1_router.include_router(create_workout_router())
    v1_router.include_router(create_items_router())
    api_router.include_router(v1_router)
    return api_router
