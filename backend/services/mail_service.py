from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

class MailService:
    """MailService."""
    
    def send_order_email(self,user_data, order_data):
        
        context = {
            'user': user_data,
            'order': order_data,
        }
        html_message = render_to_string('order_email_new.html', context)
        
        from_email = settings.EMAIL_HOST_USER  
        recipient_list = [from_email]
        email = EmailMessage(
            'Новый заказ',
            html_message,
            from_email,
            recipient_list,
        )
        email.content_subtype = 'html'  

        email.send()