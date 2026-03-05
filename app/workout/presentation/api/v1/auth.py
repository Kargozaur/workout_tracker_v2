from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.workout.application.auth.user_interactor import RegisterUser
from app.workout.application.common.status_codes import success_status_codes
from app.workout.domains.entities.user_schemas import CreateUser, GetUser


def create_register_interactor() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])

    @router.post(
        "/register",
        response_model=GetUser,
        status_code=success_status_codes.success,
    )
    @inject
    async def register_user(
            user_data: CreateUser, interactor: FromDishka[RegisterUser]
    ) -> GetUser:
        user = await interactor.execute(user_data)
        return user

    return router
