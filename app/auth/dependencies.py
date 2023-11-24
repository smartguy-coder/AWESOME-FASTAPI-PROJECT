from fastapi import Request, HTTPException, status, Depends

from app.auth import auth_lib
import dao


async def get_token_web(request: Request):
    token = request.cookies.get('token')
    return token


async def get_current_user_id_optional(token=Depends(get_token_web)):
    payload = await auth_lib.AuthHandler.decode_token_web(token)
    user_id = payload.get('user_id')
    if not user_id:
        return None
    user = await dao.get_user_by_id(int(user_id))
    if not user:
        return None
    return user_id


async def check_if_user_authenticated(token=Depends(get_token_web)):
    payload = await auth_lib.AuthHandler.decode_token_web(token)
    is_authorised = payload.get('is_authorised')
    return is_authorised
