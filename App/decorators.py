from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def verification_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/user/unverified'):
    decorator = user_passes_test(
        lambda u: u.verification.email_verified,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return decorator(function)
    return decorator
