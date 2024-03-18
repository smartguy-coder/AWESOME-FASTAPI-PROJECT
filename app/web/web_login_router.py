from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.otp_module import OneTimePassword
from app.auth.security_lib import SecurityHandler
from app.bl import user as user_bl
from app.database import get_async_session
from app.models.user import User

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates" / "web" / "login")
router = APIRouter(include_in_schema=False)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")
        self.token = form.get("auth_code")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if len(self.token) != OneTimePassword.TOKEN_LENGTH:
            self.errors.append("Enter valid token")
        if not self.errors:
            return True
        return False


@router.get("/login/")
@router.post("/login/")
async def login(request: Request, session: AsyncSession = Depends(get_async_session)):
    if request.method == "GET":
        return templates.TemplateResponse("login.html", {"request": request})

    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        valid_password, valid_token = None, None
        try:
            user: User = await user_bl.get_user_by_email(form.email, session=session)
            if user:
                valid_password = await SecurityHandler.verify_password(form.password, user.hashed_password)
                valid_token = await OneTimePassword.verify_otp(user.otp_secret, form.token)

            if not all([user, valid_password, valid_token]):
                form.__dict__.get("errors").append("Incorrect credentials")
                return templates.TemplateResponse("login.html", form.__dict__)

            return templates.TemplateResponse("home/index.html", {"request": request, "email": user.email})
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)
