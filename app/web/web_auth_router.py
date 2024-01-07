from typing import List
from typing import Optional
import re
from io import BytesIO
import base64
from app import exceptions
from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security_lib import SecurityHandler
from app.database import get_async_session
from app.bl import user as user_bl
from pathlib import Path
from fastapi import Request, status
from fastapi.templating import Jinja2Templates
import pyqrcode
from app.tasks import background_emails

from pydantic import BaseModel, validate_email

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates" / "web" / "auth")
router = APIRouter(include_in_schema=False)

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class UserCreate(BaseModel):
    email: str
    password: str
    secret: str


class ShowUser(BaseModel):
    email: str

    class Config:
        from_attributes = True


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.name: Optional[str] = None
        self.password: Optional[str] = None
        self.confirm_password: Optional[str] = None
        self.hashed_password: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.name = form.get("name")
        self.password = form.get("password") or ""
        self.confirm_password = form.get("confirm_password")
        self.hashed_password = await SecurityHandler.get_password_hash(self.password)

    async def is_valid(self):
        if not re.fullmatch(email_regex, self.email):
            # validate_email(self.email)  # use this
            self.errors.append("Please enter valid email")
        if not self.password or not len(self.password) >= 8:
            self.errors.append("Password must be > 8 chars")
        if self.password != self.confirm_password:
            self.errors.append("Confirm Password does not match")
        if not self.errors:
            return True
        return False


@router.get("/signup/", description='registration step 1')
def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup/", description='registration step 2')
async def register(request: Request, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_async_session)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = await user_bl.create_user(
                name=form.name,
                email=form.email,
                hashed_password=form.hashed_password,
                use_two_factor_auth=True,
                session=session,
            )
            data = 'otpauth://totp/FastAPI-2FA:{0}?secret={1}&issuer=FastAPI-2FA'.format(user.email, user.otp_secret)
            url = pyqrcode.create(data)
            stream = BytesIO()
            url.png(stream, scale=4, module_color=(0, 0, 0, 255), background=(255, 255, 255, 255))

            background_tasks.add_task(
                background_emails.send_email_verification,
                user_email=user.email,
                user_uuid=user.user_uuid,
                user_name=user.name,
                host=request.base_url,
            )

            return templates.TemplateResponse("qrcode.html", {"request": request,
                                                              "data": base64.b64encode(stream.getvalue()).decode(
                                                                  'utf-8')})
        except exceptions.DuplicatedEntryError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("signup.html", form.__dict__)
    return templates.TemplateResponse("signup.html", form.__dict__)


@router.get("/qrcode")
async def register(request: Request):
    return templates.TemplateResponse("qrcode/qrcode.html", {"request": request})
