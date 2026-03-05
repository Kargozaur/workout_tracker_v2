from fastapi import APIRouter

from app.workout.presentation.api.v1.auth import create_auth_interactor


def create_api_router() -> APIRouter:
    api_router = APIRouter(prefix="/api")
    v1_router = APIRouter(prefix="/v1", tags=["v1"])
    v1_router.include_router(create_auth_interactor())
    api_router.include_router(v1_router)
    return api_router
