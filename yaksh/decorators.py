from django.shortcuts import render_to_response
from django.template import RequestContext

from sbhs_server import settings


def email_verified(func):
    """ This decorator is used to check if email is verified. 
        If email is not verified then redirect user for email
        verification
    """

    def is_email_verified(request, *args, **kwargs):
        ci = RequestContext(request)
        user = request.user
        context = {}
        if not settings.is_production:
            if user.is_authenticated() and hasattr(user, 'profile'):
                if not user.profile.is_email_verified:
                    context['success'] = False
                    context['msg'] = "Your account is not verified. \
                                        Please verify your account"
                    return render_to_response('yaksh/activation_status.html',
                                                context)
        return func(request, *args, **kwargs)
    return is_email_verified
