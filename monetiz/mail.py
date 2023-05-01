from django.core.mail import send_mail

def send_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        'no-reply@petitelectronique.site',
        [str(to_email)],
        False, #fail_silently=False
    )