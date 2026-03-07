from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response

from app.workout.application.auth.commands.login_interactor import (
    LoginInteractor,
)
from app.workout.application.auth.commands.logout_global_interactor import (
    LogoutGlobalInteractor,
)
from app.workout.application.auth.commands.logout_interactor import (
    LogoutInteractor,
)
from app.workout.application.auth.commands.refresh_token_interactor import (
    RefreshTokenInteractor,
)
from app.workout.application.auth.commands.registry_interactor import (
    RegisterUser,
)
from app.workout.application.auth.commands.update_profile_interactor import (
    UpdateProfileInteractor,
)
from app.workout.application.auth.queries.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.common.status_codes import success_status_codes
from app.workout.domains.entities.user_schemas import (
    CreateUser,
    LoginSchema,
    UpdateUser,
)
from app.workout.presentation.api.annotated.oauth import Form_data, OAuth2
from app.workout.presentation.schemas.logout_schema import LogoutSchema
from app.workout.presentation.schemas.token_schema import TokenResponse
from app.workout.presentation.schemas.user_schema import GetUser


def create_auth_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])

    @router.post(
        "/register",
        response_model=GetUser,
        status_code=success_status_codes.success,
        description="created user based on provided data."
        "first name and last name may be skipped."
        "They will be parsed from an email if skipped",
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
        description="Logins user based on provided email and password."
        "Sets access and refresh tokens in both headers and cookies."
        "Returns access token and token type",
    )
    @inject
    async def login_user(
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
        "/me",
        response_model=GetUser,
        status_code=success_status_codes.ok,
        description="Retrieves user data based on token decrypted data."
        "Returns id, email, first name, last name, created at and updated at",
    )
    @inject
    async def get_me(
        _: OAuth2, interactor: FromDishka[GetUserInteractor]
    ) -> GetUser:
        return await interactor.execute()

    @router.put(
        "/me/update_profile",
        status_code=success_status_codes.success,
        response_model=GetUser,
    )
    @inject
    async def update_profile(
        _: OAuth2,
        interactor: FromDishka[UpdateProfileInteractor],
        new_data: UpdateUser,
    ) -> GetUser:
        return await interactor.execute(new_data)

    @router.post(
        "/logout",
        status_code=success_status_codes.ok,
        response_model=LogoutSchema,
    )
    @inject
    async def logout(
        _: OAuth2, interactor: FromDishka[LogoutInteractor], response: Response
    ) -> dict[str, str]:
        await interactor.execute()
        response.delete_cookie(
            key="refresh_token", httponly=True, samesite="lax"
        )
        response.delete_cookie(
            key="access_token", httponly=True, samesite="lax"
        )
        return {"Success": "You have been logged out"}

    @router.post(
        "/logout/all",
        status_code=success_status_codes.ok,
        response_model=LogoutSchema,
        description="Logout's user from all devices"
        "(removes all occurrences of refresh tokens in a database based on user id)",
    )
    @inject
    async def logout_all(
        _: OAuth2,
        interactor: FromDishka[LogoutGlobalInteractor],
        response: Response,
    ) -> dict[str, str]:
        await interactor.execute()
        response.delete_cookie(
            key="refresh_token", httponly=True, samesite="lax"
        )
        response.delete_cookie(
            key="access_token", httponly=True, samesite="lax"
        )
        return {"Success": "You have been logged out"}

    @router.post(
        "/refresh",
        response_model=TokenResponse,
        include_in_schema=False,
        status_code=success_status_codes.success,
        description="Endpoint to refresh access token"
        "(and refresh token if there is small ttl remaining).",
    )
    @inject
    async def get_token(
        _: OAuth2,
        interactor: FromDishka[RefreshTokenInteractor],
        response: Response,
    ) -> TokenResponse:
        access_token, refresh_token = await interactor.execute()
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",
            max_age=1800,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            max_age=604800,
        )
        return TokenResponse(access_token=access_token)

    return router
