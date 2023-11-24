# User sing up
1. `/api/register/` sends `register.html` to user in `api_router`
2. from `register.html` user data goes to `/api/register-final/`
3. in `/api/register-final/`:
    * checking if user with login already exists in `dao.py`
    * creating user in database in `dao.py`
    * creating otp qr code in `otp.py`
    * `/api/register-final/` sends `register_otp.html` to user
4. from `register_otp.html` user data goes to `/api/register-final-otp/`
5. in `/api/register-final-otp/`:
    * check otp password in `otp.py`
    * setting cookie in website
    * redirecting user to `/api/menu`
# User log in

1. `/api/login/` sends `login.html` to user
2. from `login.html` user data goes to `/api/login-final/`
3. in `/api/login-final/`:
    * check user password and login in `auth_lib.py`
    * `/api/login-final/` sends `login_otp.html` to user
4. from `login_otp.html` user data goes to `/api/login-final-otp/`
5. in `/api/login-final-otp/`:
    * check otp password in `otp.py`
    * setting cookie in website
    * redirecting user to `/api/menu`

# User log out
Deleting cookie