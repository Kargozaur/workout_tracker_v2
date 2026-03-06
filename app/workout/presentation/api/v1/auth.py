from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response

from app.workout.application.auth.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.auth.login_interactor import LoginInteractor
from app.workout.application.auth.registry_interactor import RegisterUser
from app.workout.application.common.status_codes import success_status_codes
from app.workout.domains.entities.user_schemas import CreateUser, LoginSchema
from app.workout.presentation.api.annotated.oauth import Form_data, OAuth2
from app.workout.presentation.schemas.token_schema import TokenResponse
from app.workout.presentation.schemas.user_schema import GetUser


def create_auth_router() -> APIRouter:
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

    @router.post(
        "/login",
        status_code=success_status_codes.success,
        response_model=TokenResponse,
    )
    @inject
    async def login_user(
            _: OAuth2,
            form_data: Form_data,
            interactor: FromDishka[LoginInteractor],
            response: Response,
    ) -> TokenResponse:
        login_schema = LoginSchema(
            email=form_data.username, password=form_data.password
        )
        access_token, refresh_token = await interactor.execute(login_schema)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            max_age=604800,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",
            max_age=1800,
        )
        return TokenResponse(access_token=access_token)

    @router.get(
        "/me", response_model=GetUser, status_code=success_status_codes.ok
    )
    @inject
    async def get_me(
            _: OAuth2, interactor: FromDishka[GetUserInteractor]
    ) -> GetUser:
        return await interactor.execute()

    return router
