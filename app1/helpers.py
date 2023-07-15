from django.core.mail import send_mail

from django.conf import settings
def send_forget_password_mail(femail , token):
    print(femail)
    subject='Your forget password link'
    message=f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token+femail}/'
    print(message)
    email_from= settings.EMAIL_HOST_USER
    recipeient_list=[femail]
    send_mail(subject,message,email_from,recipeient_list)
    return True