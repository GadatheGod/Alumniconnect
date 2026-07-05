from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    @staticmethod
    def send_otp(email, code):
        subject = 'AlumniConnect — Your OTP Code'
        message = f'''
Hello,

Your OTP code for AlumniConnect registration is: {code}

This code expires in 10 minutes.

If you didn't request this, you can ignore this email.

Regards,
AlumniConnect Team
        '''
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
