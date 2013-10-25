from em import *
from models import User, Token, Global
import uuid

def registration_key():
    return uuid.uuid4().hex


def email_subscribed(user):
    body = "Hey! Listen.fm is a free music app that gives you access to millions of song"
    body += "We're launching soon!"
    send_email("Lsten.fm, all the music.", body, user.email)


def email_key(user):
    token = Token(key=registration_key(),
                email=user.email)
    g = Global.objects()[0]
    g.n_tokens += 1
    g.save()
    token.save()

    body = "Hey! Create an account by clicking on the link below:"
    body += "localhost:5000/createAccount?accountEmail={0}&signupToken={1}".format(user.email, token.key)
    send_email("Lsten.fm, all the music.", body, user.email)


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


