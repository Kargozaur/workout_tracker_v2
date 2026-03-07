from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response

from app.workout.application.auth.commands.logout_global_interactor import (
    LogoutGlobalInteractor,
)
from app.workout.application.auth.commands.logout_interactor import (
    LogoutInteractor,
)
from app.workout.application.auth.commands.update_profile_interactor import (
    UpdateProfileInteractor,
)
from app.workout.application.auth.queries.get_current_user_interactor import (
    GetUserInteractor,
)
from app.workout.application.common.status_codes import success_status_codes
from app.workout.domains.entities.user_schemas import (
    UpdateUser,
)
from app.workout.presentation.api.annotated.oauth import OAuth2
from app.workout.presentation.schemas.logout_schema import LogoutSchema
from app.workout.presentation.schemas.user_schema import GetUser


def create_user_router() -> APIRouter:
    router = APIRouter(prefix="/user", tags=["User"])

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

    return router
