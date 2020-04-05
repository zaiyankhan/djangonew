from django.db import close_old_connections, connection
from uwsgidecorators import cron
from importlib import import_module

__author__ = "ckopanos"


def close_database_connections():
    connection.close()
    close_old_connections()

@cron(40, 3, -1, -1, -1)
def clear_django_session(args):
    from django.conf import settings
    close_database_connections()
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
        print('Cleared expired sessions')
    except NotImplementedError:
        # engine does not support clearing
        pass
    except Exception as e:
        # any other exception
        print("Error clearing session store %s" % str(e))


@cron(40, 3, -1, -1, -1)
def clear_old_cart_items(args):
    from django.conf import settings
    close_database_connections()
    from datetime import datetime, timedelta
    last_month = datetime.today() - timedelta(days=30)
    from website.models import OrderCart
    for order_cart in OrderCart.objects.filter(updated_at__lte=last_month):
        order_cart.delete()



@cron(40, 1, -1, -1, -1)
def sync_mailchimp_users(args):
    from mailchimp3 import MailChimp
    from django.conf import settings
    close_database_connections()
    client = MailChimp(settings.MAILCHIMP_USER_NAME, settings.MAILCHIMP_API_KEY)
    from website.models import AppUser
    users = AppUser.objects.filter(synced_with_mailchimp=False, is_active=True, receive_newsletter=True)
    for user in users:
        try:
            client.lists.members.create(settings.MAILCHIMP_LIST_ID, {
                'email_address': user.email,
                'status': 'subscribed',
                'merge_fields': {
                    'FNAME': user.first_name,
                    'LNAME': user.last_name,
                },
            })
            user.synced_with_mailchimp = True
            user.save()
            print("Synced user %s with mailchimp" % user.email)
        except Exception as e:
            print("Problem syncing user %s with mailhimp %s" % (user.email, str(e)))