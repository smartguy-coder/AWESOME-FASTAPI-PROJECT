from fastapi import BackgroundTasks
from app.settings import settings
from app.models.user import User
from app.utils.email.fastapi_mail_solution.email_library import send_email
from app.utils.email.fastapi_mail_solution.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD


async def send_account_verification_email(user: User, host: str, background_tasks: BackgroundTasks):
    from app.auth.security_lib import SecurityHandler
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = await SecurityHandler.get_password_hash(string_context)
    activate_url = f"{host}/auth/account-verify?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification.html",
        context=data,
        background_tasks=background_tasks
    )


async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks
    )


# async def send_password_reset_email(user: User, background_tasks: BackgroundTasks):
#     from app.config.security import hash_password
#     string_context = user.get_context_string(context=FORGOT_PASSWORD)
#     token = hash_password(string_context)
#     reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
#     data = {
#         'app_name': settings.APP_NAME,
#         "name": user.name,
#         'activate_url': reset_url,
#     }
#     subject = f"Reset Password - {settings.APP_NAME}"
#     await send_email(
#         recipients=[user.email],
#         subject=subject,
#         template_name="user/password-reset.html",
#         context=data,
#         background_tasks=background_tasks
#     )
