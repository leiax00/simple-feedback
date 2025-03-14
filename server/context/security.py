from fastapi_login import LoginManager

from server.context.config import config

manager = LoginManager(
    config.auth_salt,
    use_cookie=False,
    use_header=True,
    token_url=config.auth_api,
    default_expiry=config.auth_expiry
)


@manager.user_loader()
def load_user(username: str):
    return username
    # with database.context() as db:
    # return service.user.get_user_by_username(username, db)
