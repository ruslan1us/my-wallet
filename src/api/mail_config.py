from fastapi_mail import ConnectionConfig

from src.config import MAIL_FROM, MAIL_USERNAME, MAIL_PORT, MAIL_PASSWORD, MAIL_SERVER, MAIL_FROM_NAME

from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='src/templates',
)
