from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Subscriber, NewsletterContent
from django.conf import settings

def send_last_emails():
    subscribers = list(Subscriber.objects.values_list('email', flat=True))
    new_articles = NewsletterContent.objects.filter(is_sent=False).order_by('-created_at')[:2]

    if not new_articles.exists() or not subscribers:
        return
    
    for article in new_articles:
        context = {'subject': article.subject, 'body': article.body}
        html_content = render_to_string('email_template.html', context)
        text_content = strip_tags(html_content) 

        email = EmailMultiAlternatives(
            subject=article.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        article.is_sent = True
        article.save()
