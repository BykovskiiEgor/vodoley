from django.core.mail import send_mail

def send_password_email(email: str, password: str) -> None:
    subject = 'Ваш временный пароль'
    message = f'Ваш пароль для входа: {password}'
    send_mail(
        subject,
        message,
        from_email='bykovsky.egor2017@yandex.ru',
        recipient_list=[email]
    )