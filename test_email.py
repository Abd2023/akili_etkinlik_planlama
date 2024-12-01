from django.core.mail import send_mail
from django.conf import settings
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akili_etkinlik_planlama.settings')
django.setup()


def test_email():
    send_mail(
        'Test Email',
        'This is a test email sent from Django.',
        settings.EMAIL_HOST_USER,
        ['abdullahamin2023@gmail.com'],
        fail_silently=False,
    )

if __name__ == "__main__":
    test_email()
