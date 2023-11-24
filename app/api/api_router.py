from fastapi import APIRouter, Request, Form, Depends
from fastapi_versioning import version
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app import settings
from dao import get_user_by_login, create_user, get_user_id_by_login, get_user_uuid_by_id
from app.settings import Item
from pydantic import EmailStr
from app.auth.otp import create_qr, verify_otp
from app.auth.auth_lib import AuthHandler, AuthLibrary
from app.auth.dependencies import get_current_user_id_optional

router = APIRouter(
    prefix='/api',
    tags=['landing'],
)
templates = Jinja2Templates(directory='app//templates')


async def check_register(user_id=Depends(get_current_user_id_optional)):
    if not user_id or user_id == None:
        response = RedirectResponse('/api/sing_in_or_sing_up', status_code=302, headers=None, background=None)
        return response
    return False


@router.get('/sing_in_or_sing_up')
def sing_in_or_sing_up(request: Request):
    context = {
        'request': request,
        'title': 'Otp authentication!',

    }
    response = templates.TemplateResponse(
        'sing_in_or_sing_up.html',
        context=context,
    )
    return response


@router.get('/menu')
async def get_menu(request: Request, user_id=Depends(get_current_user_id_optional), check_id=Depends(check_register)):
    if check_id:
        return check_id
    context = {
        'request': request,
        'title': 'Menu',
        'user_id': user_id
    }
    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )


@router.get('/about')
@version(1)
async def about(request: Request, check_id=Depends(check_register)) -> dict:
    if check_id:
        return check_id
    item = Item()
    item_dict = item.to_dict()
    item_dict.delete_cookie('token')
    return item_dict


@router.get('/register')
@version(1)
async def register(request: Request):

    context = {
        'request': request,
        'title': 'Sign up',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )


@router.post('/register-final')
async def register_final(request: Request,
                         name: str = Form(),
                         user_login: EmailStr = Form(),
                         password: str = Form(),
                         password2: str = Form(),
                         ):
    is_identical = (password == password2)
    if not is_identical:
        context = {
            'request': request,
            'title': 'Sign up',
            'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
            'warning': 'Passwords are not same!',
        }

        return templates.TemplateResponse(
            'register.html',
            context=context,
        )
    is_login_already_used = await get_user_by_login(user_login)
    if is_login_already_used:
        context = {
            'request': request,
            'title': 'Sign up',
            'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
            'warning': 'Login is already used!',
        }
        return templates.TemplateResponse(
            'register.html',
            context=context,
        )
    hashed_password = await AuthHandler.get_password_hash(password)
    user_data = await create_user(
        name=name,
        login=user_login,
        password=hashed_password,)
    user_id = await get_user_id_by_login(user_login)
    token = str(await AuthHandler.encode_token(user_id, False))
    user_uuid_str = str(await get_user_uuid_by_id(user_id))
    await create_qr(user_uuid_str=user_uuid_str, user_id=user_id)
    context = {
        'request': request,
        'title': 'Otp authentication!',
        'user_id': user_id,
    }
    response = templates.TemplateResponse(
        'register_otp.html',
        context=context,
    )
    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.post('/register-otp-final')
@version(1)
async def register_otp_final(request: Request,
                             otp_password_input: int = Form(),
                             user_id=Depends(get_current_user_id_optional),
                             check_id = Depends(check_register),
                             ):
    
    user_uuid_str = str(await get_user_uuid_by_id(user_id))
    is_correct = await verify_otp(otp_password_input, user_uuid_str)
    if not is_correct:
        context = {
            'request': request,
            'title': 'Otp authentication!',
            'warning': 'Otp is not correct!',
            'user_id': user_id,
        }
        response = templates.TemplateResponse(
            'register_otp.html',
            context=context,
        )
        response.delete_cookie('token')
        token = await AuthHandler.encode_token(user_id, False)
        response.set_cookie(key='token', value=token, httponly=True)
        return response
    response = RedirectResponse('/api/menu', status_code=302, headers=None, background=None)
    token = str(await AuthHandler.encode_token(user_id, True))
    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.get('/login')
async def login(request: Request):
    context = {
        'request': request,
        'title': 'Log in',
    }
    return templates.TemplateResponse(
        'login.html',
        context=context,
    )


@router.post('/login-final')
async def register_final(request: Request,
                         user_login: EmailStr = Form(),
                         password: str = Form(),):
    if not AuthLibrary.authenticate_user(user_login, password):
        context = {
            'request': request,
            'title': 'Sign up',
            'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
            'warning': 'Log in or password is not working!',
        }
        return templates.TemplateResponse(
            'login.html',
            context=context,
        )
    user_id = await get_user_id_by_login(user_login)
    token = await AuthHandler.encode_token(user_id, False)
    context = {
        'request': request,
        'title': 'Log in using otp',
        'user_id': user_id,
    }
    response = templates.TemplateResponse(
        'login_otp.html',
        context=context,
    )
    response.delete_cookie('token')
    response.set_cookie(key='token', value=token, httponly=True)

    return response


@router.post('/login-otp-final')
@version(1)
async def register_otp_final(request: Request,
                             otp_password_input: int = Form(),):
    user = Depends(await get_current_user_id_optional(request))
    user_uuid_str = str(await get_user_uuid_by_id(user.id))
    is_correct = await verify_otp(otp_password_input, user_uuid_str)
    if not is_correct:
        context = {
            'request': request,
            'title': 'Otp authentication!',
            'warning': 'Otp password is not correct',
            'user': user,
        }

        response = templates.TemplateResponse(
            'login_otp.html',
            context=context,
        )
        token = await AuthHandler.encode_token(user.id, False)
        response.set_cookie(key='token', value=token, httponly=True)
        return response
    response = RedirectResponse('/api/register', status_code=302, headers=None, background=None)
    token = await AuthHandler.encode_token(user.id, True)
    response.set_cookie(key='token', value=token, httponly=True)
    return response


@router.get('/logout')
async def logout(request: Request):
    response = RedirectResponse('/api/register', status_code=302, headers=None, background=None)
    response.delete_cookie('token')
    return response

