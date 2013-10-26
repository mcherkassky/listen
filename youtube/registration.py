from em import *
from models import User, Token, Global
import uuid

def registration_key():
    return uuid.uuid4().hex


def email_subscribed(user):
    body = "<h4> Welcome to Listen.fm </h4>" \
           "<br>" \
           "<div>We are a next generation streaming service giving you access to millions of songs.</div>" \
           "<br>" \
           "<div> Check your email in the next couple of days for an access key.</div>"
    send_email("Listen.fm, all the music.", body, user.email)


def email_key(user):
    token = Token(key=registration_key(),
                email=user.email)
    g = Global.objects()[0]
    g.n_tokens += 1
    g.save()
    token.save()

    body = "<h4> Welcome to Listen.fm </h4>" \
           "<br>" \
           "We are a next generation streaming service giving you access to millions of songs.</div>" \
           "<br>" \
           "Create an account by clicking on the link below:" \
           "<br>" \
           "<a href='listenapp.herokuapp.com/createAccount?accountEmail={0}&signupToken={1}'.format(user.email, token.key) > Register for Listen.fm</a>"
    send_email("Listen.fm, all the music.", body, user.email)


def keys_available():
    """Returns true if keys can be generated.
    """
    try:
        g = Global.objects()
        g = g[0]
        return g.n_tokens < 100
    except:
        g = Global(n_tokens=0)
        g.save()
        return True

def clear_keys():
    Token.objects.delete()
    g = Global.objects()[0]
    g.n_tokens = 0
    g.save()


