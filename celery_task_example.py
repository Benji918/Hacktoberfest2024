from celery import shared_task
from core.models import MessageBoard
from django.conf import settings
from datetime import datetime
from django.template.loader import get_template
from django.core.mail import EmailMessage

@shared_task(name='email_newsletter')
def send_newsletter():
    subject = "Your Monthly Newsletter"
    
    subscribers = MessageBoard.objects.get(id=1).subscribers.filter(
        newsletter_subscribed=True,
    )
    
    for subscriber in subscribers:
        print(subscriber.email)
        message = get_template('newsletter.html').render(context={'name': subscriber.username})
        mail = EmailMessage(
            subject=subject, 
            body=message, 
            from_email=settings.EMAIL_HOST_USER,
            to=[subscriber.email],
            reply_to=[settings.EMAIL_HOST_USER],
            )
        mail.content_subtype = "html"
        mail.send()
    
    current_month = datetime.now().strftime('%B')
    subscriber_count = subscribers.count()   
    return f'{current_month} Newsletter to {subscriber_count} subs'
