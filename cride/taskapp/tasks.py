"""Celery tasks"""


#Django
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

#Models
from cride.users.models import User
from cride.rides.models import Ride

#utils
import time
import jwt
from datetime import timedelta

#celery
from celery.decorators import task, periodic_task

def gen_verification_token(user):
    """Create JWT token that the users can use to verify accounts"""
    exp_date = timezone.now() +  timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': (exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link tho the provided user"""
    for i in range(30):
        time.sleep(1)
        print("Sleeping", str(i + 1))
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}: before starts using Comparte Ride you have to verify your email'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user':user }
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()

@periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=30))
def disable_finished_rides():
    """Disable finished rides"""
    now = timezone.now()
    offset = now + timedelta(minutes=30)

    rides = Ride.objects.filter(arrival_date__gte=now, arrival_date__lte=offset, is_active=True)
    rides.update(is_active=False)
