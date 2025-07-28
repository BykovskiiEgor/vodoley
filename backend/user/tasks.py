from shop.celery import app
from user.mailer import send_password_email

@app.task()
def send_email_task(email: str, password: str) -> None:
    """Task for send email with password."""
    try:
        send_password_email(email, password)
    except Exception as e:
        raise e